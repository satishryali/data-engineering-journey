"""Idempotent checkpoint bridge. Only the existing coach writes learning authorities."""
from contextlib import contextmanager
import json
import os
from pathlib import Path
import tempfile
import re
from services.records import Records, load_coach, now


@contextmanager
def writer_lock(root):
    path = root / 'apps/recalllab/data/writer.lock'
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open('a+b') as f:
        f.seek(0)
        f.write(b'0')
        f.flush()
        f.seek(0)
        if os.name == 'nt':
            import msvcrt
            msvcrt.locking(f.fileno(), msvcrt.LK_NBLCK, 1)
        else:
            import fcntl
            fcntl.flock(f, fcntl.LOCK_EX | fcntl.LOCK_NB)
        try:
            yield
        finally:
            f.seek(0)
            if os.name == 'nt':
                msvcrt.locking(f.fileno(), msvcrt.LK_UNLCK, 1)
            else:
                fcntl.flock(f, fcntl.LOCK_UN)


def immutable_evidence(root, relative, payload):
    if not re.fullmatch(r'apps/recalllab/evidence/ATT-RL-[a-f0-9]{32}\.json', relative):
        raise ValueError('Invalid immutable attempt evidence path')
    target = root / relative
    target.parent.mkdir(parents=True, exist_ok=True)
    text = json.dumps(payload, ensure_ascii=False, indent=2) + '\n'
    if target.exists():
        if target.read_text(encoding='utf-8') != text:
            raise ValueError('Existing attempt evidence differs; preserve and reconcile it')
        return
    # Atomic rename: an interruption cannot expose a partially written evidence file.
    fd, tmp = tempfile.mkstemp(dir=target.parent, suffix='.tmp')
    try:
        with os.fdopen(fd, 'w', encoding='utf-8', newline='\n') as f:
            f.write(text)
            f.flush()
            os.fsync(f.fileno())
        os.replace(tmp, target)
    finally:
        if os.path.exists(tmp):
            os.unlink(tmp)


def end_session(records, journal, session):
    root = records.root
    with writer_lock(root):
        coach = load_coach(root)
        coach.recover(root)
        with journal.db() as db:
            db.execute('BEGIN IMMEDIATE')
            row = db.execute('SELECT * FROM sessions WHERE id=?', (session,)).fetchone()
            if not row:
                raise ValueError('Unknown session')
            if row['state'] == 'recorded':
                return 'Already recorded in canonical tracker'
            if row['batch']:
                batch = json.loads(row['batch'])
            else:
                attempts = sorted(journal.effective_attempts(session),key=lambda a:(a['attempt_date_ist'],a['timestamp'],a['attempt_id']))
                if not attempts:
                    raise ValueError('No submitted answers. Opening the site is not a learning event.')
                queue = {r['item_id']: r for r in records.csv('revision-queue.csv')}
                reviews, skills, mistakes = [], [], []
                known_mistakes = records.json('tracking/mistakes.json')['mistakes']
                for a in attempts:
                    relative = f'apps/recalllab/evidence/{a["attempt_id"]}.json'
                    immutable_evidence(root, relative, a)
                    last = queue[a['item_id']]['last_attempt_date']
                    kind = ('application' if a.get('manual_assessment') and last else 'diagnostic' if a.get('manual_assessment') else
                            'immediate_correction' if a.get('correction_of') and last else 'diagnostic' if not last else
                            'delayed' if a['attempt_date_ist'] > last else 'application' if a.get('assessment_kind') == 'application' else 'immediate_correction')
                    queue[a['item_id']]['last_attempt_date'] = a['attempt_date_ist']
                    review = dict(a, evidence=relative, review_kind=kind, topic_ids=[])
                    reviews.append(review)
                    if a.get('score') is not None:
                        skills.append({'observation_id': 'OBS-' + a['attempt_id'], 'item_id': a['item_id'],
                                       'dimension': a['dimension'], 'state': a['result'] if a['result'] != 'unknown' else 'unassessed',
                                       'observed_date_ist': a['attempt_date_ist'], 'evidence': relative, 'help_used': a['help_used']})
                    # Only objective observed failures create mistakes, never manual/unassessed work.
                    if (a.get('score') == 0 or a.get('correct') is False) and a.get('evaluation') in ('exact_output', 'sql_fixtures', 'human_review'):
                        import copy
                        mistake_id = 'M-RL-' + a['evaluation'] + '-' + a['item_id']
                        existing = next((m for m in known_mistakes if m['mistake_id'] == mistake_id), None)
                        if existing:
                            m = copy.deepcopy(existing)
                            m['observations'] = []
                        else:
                            is_concept = a['item_id'] not in ('PY-001', 'PY-002', 'SQL-001', 'SQL-002', 'SQL-003')
                            m = {'mistake_id': mistake_id, 'category': 'conceptual',
                                 'topic_ids': [a['item_id']] if is_concept else [],
                                 'exercise_ids': [] if is_concept else [a['item_id']], 'wording': 'Observed automatic fixture/output mismatch',
                                 'observed_behaviour': a['feedback'], 'expected_behaviour': 'Match the controlled task output and explain the result.',
                                 'cause': {'confidence': 'hypothesis', 'description': 'Cause not established by output comparison alone.'},
                                 'correction_and_assistance': 'Help is recorded on the assessment; no correction verified.',
                                 'follow_up_task': 'Trace the failed example and attempt a changed variation.', 'linked_review_items': [a['item_id']],
                                 'verification_review_id': None, 'observations': []}
                        m['status'] = 'practising'
                        m['observations'].append({'attempt_id': a['attempt_id'], 'observed_date_ist': a['attempt_date_ist'],
                                                  'evidence': relative, 'observation': a['feedback']})
                        mistakes.append(m)
                recs = records.recommendations(reviews)
                summary = (f'RecallLab revision: {len(reviews)} submitted attempts; '
                           f'{sum(r.get("score") is None for r in reviews)} unscored/manual or unknown assessments. '
                           'Scores apply only to the tested dimension. Help retained in event evidence. '
                           'Review sections: ' + '; '.join(r['path'] + ' / ' + r['heading'] for r in recs) +
                           '. Current project task and study timers unchanged; see progress/current.md.')
                batch = {'checkpoint_id': 'CP-' + session, 'date_ist': now().date().isoformat(), 'kind': 'learning',
                         'summary': summary, 'evidence_ids': [r['evidence'] for r in reviews],
                         'reviews': reviews, 'skill_updates': skills, 'mistakes': mistakes}
                db.execute("UPDATE sessions SET state='pending', batch=? WHERE id=?", (json.dumps(batch), session))
        # Export/import and a crash before evidence publication must be recoverable too.
        for attempt in journal.effective_attempts(session):
            immutable_evidence(root, f'apps/recalllab/evidence/{attempt["attempt_id"]}.json', attempt)
        # A consistent pending-batch snapshot accompanies every completion attempt.
        journal.backup()
        # Coach checks note mappings before any canonical transaction; do not invent them.
        registry = coach.note_revision.sync(root, records.json('tracking/topic-map.json'), batch['date_ist'])
        coach.note_revision.check(root, registry)
        coach.record(root, batch)
        # refresh through supported transaction API, including the live inventory.
        refreshed = coach.note_revision.sync(root, records.json('tracking/topic-map.json'), batch['date_ist'])
        coach.transaction(root, {'tracking/topic-map.json': coach.dump(refreshed), **coach.views(root, registry=refreshed)})
        coach.validate(root)
        with journal.db() as db:
            db.execute("UPDATE sessions SET state='recorded' WHERE id=?", (session,))
        journal.put('settings', 'last-report', {'session_id':session, 'recommendations':records.recommendations(journal.effective_attempts(session)),
                                               'summary':batch['summary'], 'checkpoint_id':batch['checkpoint_id']})
        return 'Recorded in canonical tracker. GitHub sync requires an intentional commit/push.'
