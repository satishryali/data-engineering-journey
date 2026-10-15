"""Evidence-based checkpoint/revision helpers. Python standard library only."""

import argparse
import copy
import csv
from datetime import date, datetime, timedelta, timezone
import hashlib
import io
import json
import os
from pathlib import Path
import re


ROOT = Path(__file__).resolve().parents[1]
INTERVALS = (1, 3, 7, 14, 30)
DIMENSIONS = ('explaining', 'reading_predicting', 'modifying', 'building', 'debugging')
STATES = ('unassessed', 'needs_guidance', 'assisted', 'independent')
KINDS = ('initial_learning', 'diagnostic', 'immediate_correction', 'delayed', 'application')
HISTORY_EXTRA = ('review_id', 'attempt_id', 'review_kind', 'score', 'hints_used', 'notes_used', 'event_json')
JOURNAL = 'tracking/.coach-transaction.json'


def dump(value):
    return json.dumps(value, ensure_ascii=False, indent=2) + '\n'


def read_json(root, path):
    return json.loads((root / path).read_text(encoding='utf-8-sig'))


def read_csv(root, path):
    with (root / path).open(encoding='utf-8-sig', newline='') as stream:
        reader = csv.DictReader(stream)
        return list(reader.fieldnames or []), list(reader)


def csv_text(fields, rows):
    out = io.StringIO(newline='')
    writer = csv.DictWriter(out, fieldnames=fields, lineterminator='\n')
    writer.writeheader()
    writer.writerows(rows)
    return out.getvalue()


def sha(data):
    return hashlib.sha256(data).hexdigest()


def require(condition, message):
    if not condition:
        raise ValueError(message)


def evidence_exists(root, value):
    path = (root / value.split('#')[0]).resolve()
    return path.is_relative_to(root.resolve()) and path.is_file()


def independent(event):
    return (event.get('result') == 'independent' and event.get('help_used') is False
            and event.get('notes_used') is False and event.get('hints_used') == 0)


def schedule(stage, due, event, previous_date=None):
    """Unknown scores and immediate correction cannot change delayed review state."""
    when = date.fromisoformat(event['attempt_date_ist'])
    require(event['review_kind'] in KINDS, 'Unknown review kind')
    score = event.get('score')
    require(score is None or type(score) is int and 0 <= score <= 3, 'Score must be null or 0..3')
    if event['review_kind'] == 'delayed' and previous_date:
        require(when > date.fromisoformat(previous_date), 'Same-day work is not delayed retrieval')
    require(stage is None or type(stage) is int and 0 <= stage <= 4, 'Invalid review stage')
    if score is None or event['review_kind'] == 'immediate_correction':
        return stage, due
    if stage is None or score < 2 or not independent(event):
        stage = 0
    elif event['review_kind'] == 'delayed' and score == 3:
        stage = min(stage + 1, 4)
    return stage, (when + timedelta(days=INTERVALS[stage])).isoformat()


def upsert_mistake(items, incoming):
    """One recurrence per distinct attempt, preserving nulls and unknown fields."""
    incoming = copy.deepcopy(incoming)
    ident = incoming['mistake_id']
    prior = next((m for m in items if m['mistake_id'] == ident), None)
    if prior is None:
        items.append(incoming)
        prior = incoming
    else:
        observations = prior.setdefault('observations', [])
        for observation in incoming.get('observations', []):
            found = next((o for o in observations if o['attempt_id'] == observation['attempt_id']), None)
            require(found is None or found == observation, 'Conflicting mistake attempt ID')
            if found is None:
                observations.append(observation)
        prior.update({k: v for k, v in incoming.items() if k not in ('observations', 'first_observed', 'latest_observed', 'recurrence_count')})
    ids = [o['attempt_id'] for o in prior['observations']]
    require(len(ids) == len(set(ids)), 'Duplicate mistake observation')
    dates = [o['observed_date_ist'] for o in prior['observations']]
    require(bool(dates), 'Mistake requires actual evidence')
    prior['first_observed'], prior['latest_observed'] = min(dates), max(dates)
    prior['recurrence_count'] = len(ids)


def safe_target(root, relative):
    fixed = {'tracking/revision-queue.csv', 'tracking/revision-history.csv',
             'tracking/mistakes.json', 'tracking/skill-state.json', 'tracking/checkpoint-index.json',
             'progress/current.md', 'START-HERE.md', 'progress/session-history.md',
             'Notes/revision/topics.json', 'Notes/revision/reviews.jsonl', 'Notes/revision/mistakes.md'}
    require(relative in fixed or re.fullmatch(r'progress/weekly/\d{4}-W\d{2}\.md', relative), 'Unsupported transaction path')
    target = (root / relative).resolve()
    require(target.is_relative_to(root.resolve()), 'Path outside repository')
    return target


def recover(root):
    journal = root / JOURNAL
    if not journal.exists():
        return False
    writes = read_json(root, JOURNAL)['writes']
    for rel, entry in writes.items():
        target = safe_target(root, rel)
        current = target.read_bytes() if target.exists() else None
        current_hash = sha(current) if current is not None else None
        require(current_hash in (entry['before'], sha(entry['text'].encode('utf-8'))),
                f'Concurrent edit in {rel}; preserve it and reconcile the transaction manually')
    for rel, entry in writes.items():
        target = safe_target(root, rel)
        target.parent.mkdir(parents=True, exist_ok=True)
        temporary = target.with_name(target.name + '.coach-tmp')
        temporary.write_bytes(entry['text'].encode('utf-8'))
        os.replace(temporary, target)
    journal.unlink()
    return True


def transaction(root, writes):
    require(not (root / JOURNAL).exists(), 'Interrupted batch: run coach.py recover first')
    entries = {}
    for rel, text in writes.items():
        target = safe_target(root, rel)
        before = target.read_bytes() if target.exists() else None
        if before != text.encode('utf-8'):
            entries[rel] = {'before': sha(before) if before is not None else None, 'text': text}
    if not entries:
        return
    (root / JOURNAL).write_text(dump({'writes': entries}), encoding='utf-8')
    recover(root)


def views(root, queue=None, history=None, mistakes=None):
    queue = queue if queue is not None else read_csv(root, 'tracking/revision-queue.csv')[1]
    history = history if history is not None else read_csv(root, 'tracking/revision-history.csv')[1]
    mistakes = mistakes if mistakes is not None else read_json(root, 'tracking/mistakes.json')
    registry = read_json(root, 'tracking/topic-map.json')
    by_id = {q['item_id']: q for q in queue}
    topics = []
    events = [json.loads(r['event_json']) for r in history if r.get('event_json')]
    for concept in registry['topics']:
        topic = copy.deepcopy(concept)
        row = by_id[topic['id']]
        actual = [e for e in events if e['item_id'] == topic['id']]
        topic.update(assessment_status='unassessed' if row['last_result'] == 'not_attempted' else row['last_result'],
                     interval_stage=int(row['review_stage']) if row['review_stage'] else None,
                     next_review_date=row['next_review_date_ist'] or None,
                     last_reviewed_date=actual[-1]['attempt_date_ist'] if actual else None,
                     recent_scores=[e.get('score') for e in actual[-5:]],
                     help_needed=actual[-1].get('help_used') if actual else None,
                     last_review_id=actual[-1]['review_id'] if actual else None)
        topics.append(topic)
    state = {'schema_version': 2, 'generated': True, 'timezone': 'Asia/Kolkata',
             'authoritative_queue': 'tracking/revision-queue.csv',
             'authoritative_history': 'tracking/revision-history.csv', 'topics': topics,
             'session': {'status': 'not_started', 'pending_task_source': 'progress/current.md',
                         'deferred_legacy_question_id': 'diagnostic-dict-001'}}
    lines = ['# Mistake index (generated)', '', 'Source: `tracking/mistakes.json`. Do not edit this view.', '',
             '| ID | Kind | Status | Distinct attempts | Observed behaviour | Follow-up |',
             '| --- | --- | --- | ---: | --- | --- |']
    for m in mistakes['mistakes']:
        clean = lambda x: str(x).replace('|', '/').replace('\n', ' ')
        lines.append('| ' + ' | '.join(clean(x) for x in (m['mistake_id'], m['category'], m['status'], m['recurrence_count'], m['observed_behaviour'], m['follow_up_task'])) + ' |')
    return {'Notes/revision/topics.json': dump(state),
            'Notes/revision/reviews.jsonl': ''.join(json.dumps(e, ensure_ascii=False) + '\n' for e in events),
            'Notes/revision/mistakes.md': '\n'.join(lines) + '\n'}


def record(root, batch):
    """Save one evidence batch. Timer and attempt files are deliberately not writable."""
    require(not (root / JOURNAL).exists(), 'Interrupted batch: recover first')
    ident, when = batch['checkpoint_id'], batch['date_ist']
    require(bool(re.fullmatch(r'[A-Za-z0-9._-]+', ident)), 'Invalid checkpoint ID')
    date.fromisoformat(when)
    require(batch.get('kind') in ('learning', 'setup'), 'Label learning versus setup')
    require(bool(batch.get('summary', '').strip()), 'Checkpoint summary required')
    evidence = batch['evidence_ids']
    require(bool(evidence) and len(set(evidence)) == len(evidence), 'Distinct evidence IDs required')
    for ref in evidence:
        require(evidence_exists(root, ref), f'Missing evidence: {ref}')
    index = read_json(root, 'tracking/checkpoint-index.json')
    payload_hash = sha(json.dumps(batch, sort_keys=True, ensure_ascii=False).encode('utf-8'))
    evidence_key = sha(json.dumps(sorted(evidence)).encode('utf-8'))
    for old in index['checkpoints']:
        if old['checkpoint_id'] == ident:
            require(old['sha256'] == payload_hash, 'Checkpoint ID reused with different content')
            return False
        require(old['evidence_key'] != evidence_key, 'This evidence batch is already checkpointed')
    require(batch['kind'] != 'setup' or not any(batch.get(k) for k in ('reviews', 'mistakes', 'skill_updates')),
            'Setup cannot create learning outcomes')
    qfields, queue = read_csv(root, 'tracking/revision-queue.csv')
    hfields, history = read_csv(root, 'tracking/revision-history.csv')
    by_id = {q['item_id']: q for q in queue}
    registry = read_json(root, 'tracking/topic-map.json')
    links = {t['id']: set(t['exercise_ids']) for t in registry['topics']}
    prior_events = [json.loads(r['event_json']) for r in history if r.get('event_json')]
    for event in batch.get('reviews', []):
        require(all(isinstance(event.get(key), str) and event[key].strip() for key in ('review_id', 'attempt_id', 'evidence')), 'Review and attempt IDs/evidence required')
        require(event['item_id'] in by_id, 'Unknown review item')
        require(event['evidence'] in evidence, 'Review evidence must belong to this batch')
        require(event.get('result') in ('independent', 'assisted', 'needs_guidance', 'unknown'), 'Unknown review result')
        for key in ('help_used', 'notes_used'):
            require(event.get(key) is None or type(event[key]) is bool, f'{key} must be boolean or null')
        require(event.get('hints_used') is None or type(event['hints_used']) is int and event['hints_used'] >= 0, 'Invalid hints count')
        require(event['result'] != 'independent' or independent(event), 'Independent result requires explicit no help, hints or notes')
        require(event['attempt_date_ist'] <= when, 'Future review evidence')
        for topic in event.get('topic_ids', []):
            require(topic in links and (event['item_id'] == topic or event['item_id'] in links[topic]), 'Invalid exercise/concept mapping')
        if event.get('timestamp'):
            stamp = datetime.fromisoformat(event['timestamp'].replace('Z', '+00:00'))
            require(stamp.tzinfo is not None, 'Timestamp requires timezone')
            require(stamp.astimezone(timezone(timedelta(hours=5, minutes=30))).date().isoformat() == event['attempt_date_ist'], 'Timestamp/IST date mismatch')
        existing = next((e for e in prior_events if e['review_id'] == event['review_id']), None)
        if existing:
            require(existing == event, 'Review ID reused with different content')
            continue
        require(not any(e['item_id'] == event['item_id'] and e['attempt_id'] == event['attempt_id'] for e in prior_events), 'Attempt already recorded under another review ID')
        row = by_id[event['item_id']]
        require(not row['last_attempt_date'] or event['attempt_date_ist'] >= row['last_attempt_date'], 'Older review needs explicit historical reconciliation')
        stage, due = schedule(int(row['review_stage']) if row['review_stage'] else None,
                              row['next_review_date_ist'] or None, event, row['last_attempt_date'] or None)
        row.update(last_attempt_date=event['attempt_date_ist'], last_result=event['result'],
                   review_stage='' if stage is None else str(stage), next_review_date_ist=due or '', evidence=event['evidence'],
                   status='reviewing' if stage is not None else 'learning')
        if independent(event) and event.get('score') in (2, 3) and event['review_kind'] != 'immediate_correction' and not row['first_independent_success_date']:
            row['first_independent_success_date'] = event['attempt_date_ist']
        entry = {key: '' for key in hfields}
        entry.update({k: '' if event.get(k) is None else str(event[k]) for k in hfields if k in event})
        entry['next_review_date_ist'] = due or ''
        entry['event_json'] = json.dumps(event, ensure_ascii=False, sort_keys=True)
        history.append(entry)
        prior_events.append(copy.deepcopy(event))
    mistakes = read_json(root, 'tracking/mistakes.json')
    for incoming in batch.get('mistakes', []):
        require(incoming['category'] in ('conceptual', 'debugging_approach', 'environment', 'minor_syntax'), 'Invalid mistake category')
        require(incoming['status'] in ('open', 'practising', 'verified_on_delayed_independent_practice'), 'Invalid mistake status')
        require(incoming['cause']['confidence'] in ('confirmed', 'hypothesis'), 'Invalid cause confidence')
        require(all(i in by_id for i in incoming['exercise_ids']) and all(i in links for i in incoming['topic_ids']), 'Invalid mistake mapping')
        require(all(k in incoming for k in ('observed_behaviour', 'expected_behaviour', 'correction_and_assistance', 'follow_up_task', 'linked_review_items')), 'Incomplete mistake record')
        for observation in incoming['observations']:
            date.fromisoformat(observation['observed_date_ist'])
            require(observation['observed_date_ist'] <= when, 'Future mistake observation')
            require(observation['evidence'] in evidence, 'Mistake evidence must belong to batch')
        upsert_mistake(mistakes['mistakes'], incoming)
    for mistake in mistakes['mistakes']:
        if mistake['status'] == 'verified_on_delayed_independent_practice':
            event = next((e for e in prior_events if e['review_id'] == mistake.get('verification_review_id')), None)
            require(event and independent(event) and event['review_kind'] == 'delayed' and event.get('score') in (2, 3)
                    and (event['item_id'] in mistake['exercise_ids'] or event['item_id'] in mistake['topic_ids']),
                    'Mistake verification needs relevant delayed independent evidence')
    skills = read_json(root, 'tracking/skill-state.json')
    for update in batch.get('skill_updates', []):
        require(update['item_id'] in by_id and update['dimension'] in DIMENSIONS and update['state'] in STATES, 'Invalid skill dimension/state')
        require(update['evidence'] in evidence, 'Skill evidence must belong to batch')
        date.fromisoformat(update['observed_date_ist'])
        require(update['observed_date_ist'] <= when, 'Future skill observation')
        require(update.get('help_used') is None or type(update['help_used']) is bool, 'Unknown skill help must remain null')
        same = next((o for o in skills['observations'] if o['observation_id'] == update['observation_id']), None)
        require(same is None or same == update, 'Conflicting skill observation ID')
        if same is None:
            skills['observations'].append(copy.deepcopy(update))
    summary = f'\n<!-- checkpoint:{ident} -->\n## {when} — {ident} ({batch["kind"]})\n\n{batch["summary"].strip()}\n\nEvidence: ' + '; '.join(f'`{r}`' for r in evidence) + '\n'
    daily = (root / 'progress/session-history.md').read_text(encoding='utf-8-sig')
    require(f'<!-- checkpoint:{ident} -->' not in daily, 'Daily block exists without index; recover/reconcile first')
    index['checkpoints'].append({'checkpoint_id': ident, 'date_ist': when, 'kind': batch['kind'], 'sha256': payload_hash, 'evidence_key': evidence_key})
    writes = {'tracking/revision-queue.csv': csv_text(qfields, queue),
              'tracking/revision-history.csv': csv_text(hfields, history),
              'tracking/mistakes.json': dump(mistakes), 'tracking/skill-state.json': dump(skills),
              'tracking/checkpoint-index.json': dump(index), 'progress/session-history.md': daily.rstrip() + '\n' + summary}
    require(('checkpoint_text' in batch) == ('handoff_text' in batch), 'Update checkpoint and handoff together')
    if 'checkpoint_text' in batch:
        require(batch.get('next_task') and batch['next_task'] in batch['checkpoint_text'] and batch['next_task'] in batch['handoff_text'], 'Same exact next task required in both handoffs')
        writes.update({'progress/current.md': batch['checkpoint_text'], 'START-HERE.md': batch['handoff_text']})
    writes.update(views(root, queue, history, mistakes))
    transaction(root, writes)
    return True


def status(root, when):
    date.fromisoformat(when)
    queue = read_csv(root, 'tracking/revision-queue.csv')[1]
    due = [q for q in queue if q['next_review_date_ist'] and q['next_review_date_ist'] <= when]
    due.sort(key=lambda q: (q['last_result'] not in ('needs_guidance', 'assisted'), q['next_review_date_ist'], q['item_id']))
    sessions = read_csv(root, 'tracking/study-log.csv')[1]
    monday = date.fromisoformat(when) - timedelta(days=date.fromisoformat(when).weekday())
    seconds_today = seconds_week = 0
    for row in sessions:
        if row['status'] != 'completed':
            continue
        seconds = (datetime.fromisoformat(row['end_time_ist']) - datetime.fromisoformat(row['start_time_ist'])).total_seconds()
        require(seconds >= 0, 'Negative study interval')
        if row['study_date_ist'] == when:
            seconds_today += seconds
        if monday.isoformat() <= row['study_date_ist'] <= when:
            seconds_week += seconds
    states = {q['item_id']: {d: 'unassessed' for d in DIMENSIONS} for q in queue}
    for observation in read_json(root, 'tracking/skill-state.json')['observations']:
        if observation['observed_date_ist'] <= when:
            states[observation['item_id']][observation['dimension']] = observation['state']
    changed_sources = []
    for topic in read_json(root, 'tracking/topic-map.json')['topics']:
        if any(sha((root / source['path']).read_bytes()) != source['sha256'] for source in topic['sources']):
            changed_sources.append(topic['id'])
    return {'date_ist': when, 'due_items': [q['item_id'] for q in due],
            'confirmed_today_seconds': seconds_today, 'confirmed_week_seconds': seconds_week,
            'running_or_uncertain_sessions': [r['session_id'] for r in sessions if r['status'] != 'completed'],
            'daily_learning_source': 'progress/session-history.md', 'pending_task_source': 'progress/current.md',
            'skill_dimensions': states, 'source_changes_to_inspect': changed_sources,
            'delayed_retention_source': 'tracking/revision-history.csv (review_kind=delayed only)'}


def weekly(root, week, as_of):
    start, current = date.fromisoformat(week), date.fromisoformat(as_of)
    require(start.weekday() == 0 and current >= start, 'Week must start on Monday, not after as-of date')
    end = start + timedelta(days=6)
    observed_end = min(end, current)
    rows = read_csv(root, 'tracking/study-log.csv')[1]
    seconds = sum((datetime.fromisoformat(r['end_time_ist']) - datetime.fromisoformat(r['start_time_ist'])).total_seconds()
                  for r in rows if r['status'] == 'completed' and week <= r['study_date_ist'] <= observed_end.isoformat())
    observations = [o for o in read_json(root, 'tracking/skill-state.json')['observations'] if week <= o['observed_date_ist'] <= observed_end.isoformat()]
    events = [json.loads(r['event_json']) for r in read_csv(root, 'tracking/revision-history.csv')[1] if r.get('event_json')]
    delayed = [e for e in events if e['review_kind'] == 'delayed' and week <= e['attempt_date_ist'] <= observed_end.isoformat()]
    mistakes = [m for m in read_json(root, 'tracking/mistakes.json')['mistakes'] if m['first_observed'] <= observed_end.isoformat()]
    year, number, _ = start.isocalendar()
    text = [f'# {year}-W{number:02d} learning summary', '',
            f'Generated from saved evidence as of {as_of} IST; ' + ('partial week.' if current <= end else 'reconstructed after week end.'),
            'This is a generated view, not a new learning or review event.', '',
            f'Confirmed study time: {int(seconds)//3600}h {int(seconds)%3600//60}m {int(seconds)%60}s. Running/uncertain intervals excluded.', '',
            '## Actual work and demonstrated independence', '',
            'Daily evidence: `progress/session-history.md`; underlying attempts are referenced by each observation.', '']
    for o in observations:
        text.append(f'- {o["item_id"]}, {o["dimension"]}: {o["state"]} on {o["observed_date_ist"]}; `{o["evidence"]}`. Help: {o.get("help_used")!r}.')
    if not observations:
        text.append('- No dimension-specific assessment recorded for this week; this does not establish that no study occurred.')
    text.extend(['', '## Recurring difficulties', ''])
    for m in mistakes:
        count = len([o for o in m['observations'] if o['observed_date_ist'] <= observed_end.isoformat()])
        text.append(f'- {m["mistake_id"]}: {m["observed_behaviour"]} ({count} distinct observed attempts by this date). See canonical tracker for current status and follow-up.')
    text.extend(['', '## Delayed review results', '', f'{len(delayed)} actual delayed review events in this period.'])
    for e in delayed:
        text.append(f'- {e["review_id"]}: {e["item_id"]}, {e["result"]}; score {e.get("score")!r}, `{e["evidence"]}`.')
    text.extend(['', '## Unassessed areas and next focus', '',
                 'Unobserved skill dimensions remain unassessed; note presence, time and setup are not proficiency.',
                 'Keep the latest learner-selected task in `progress/current.md`; complete its prerequisite step before returning to the full cleaner. Select a few due weak concepts rather than the whole backlog.',
                 'The tutor should interpret changes in independence from distinct dated observations, not compare hours with ability.', ''])
    relative = f'progress/weekly/{year}-W{number:02d}.md'
    transaction(root, {relative: '\n'.join(text)})
    return relative


def validate(root):
    require(not (root / JOURNAL).exists(), 'Interrupted transaction requires recovery')
    qfields, queue = read_csv(root, 'tracking/revision-queue.csv')
    ids = [q['item_id'] for q in queue]
    require(len(ids) == len(set(ids)), 'Duplicate queue ID')
    registry = read_json(root, 'tracking/topic-map.json')
    topics = {t['id']: t for t in registry['topics']}
    require(len(topics) == len(registry['topics']), 'Duplicate topic ID')
    for t in topics.values():
        require(t['id'] in ids, 'Concept has no authoritative queue row')
        require(all(i in ids for i in t['exercise_ids']), 'Unknown exercise mapping')
        require(all(i in topics for i in t['prerequisites']), 'Unknown prerequisite')
        for source in t['sources']:
            require(evidence_exists(root, source['path']), f'Missing topic source {source["path"]}')
    for row in queue:
        require(not row['review_stage'] or 0 <= int(row['review_stage']) <= 4, 'Invalid queue stage')
        for key in ('last_attempt_date', 'first_independent_success_date', 'next_review_date_ist'):
            if row[key]:
                date.fromisoformat(row[key])
    history = read_csv(root, 'tracking/revision-history.csv')[1]
    review_ids = [r['review_id'] for r in history if r.get('review_id')]
    require(len(review_ids) == len(set(review_ids)), 'Duplicate review ID')
    for row in history:
        require(row['item_id'] in ids, 'Review references unknown item')
        if row.get('event_json'):
            event = json.loads(row['event_json'])
            require(event['review_id'] == row['review_id'], 'Review payload ID mismatch')
            require(evidence_exists(root, event['evidence']), 'Review evidence file missing')
    mistakes = read_json(root, 'tracking/mistakes.json')['mistakes']
    require(len({m['mistake_id'] for m in mistakes}) == len(mistakes), 'Duplicate mistake ID')
    for m in mistakes:
        require(m['status'] in ('open', 'practising', 'verified_on_delayed_independent_practice'), 'Invalid mistake status')
        require(m['category'] in ('conceptual', 'debugging_approach', 'environment', 'minor_syntax'), 'Invalid mistake category')
        require(m['cause']['confidence'] in ('confirmed', 'hypothesis'), 'Unknown cause confidence')
        require(all(i in ids for i in m['exercise_ids']) and all(i in topics for i in m['topic_ids']), 'Invalid mistake mapping')
        require(m['recurrence_count'] == len({o['attempt_id'] for o in m['observations']}), 'Incorrect recurrence count')
        for o in m['observations']:
            date.fromisoformat(o['observed_date_ist'])
            require(evidence_exists(root, o['evidence']), 'Missing mistake evidence')
    skills = read_json(root, 'tracking/skill-state.json')
    require(len({o['observation_id'] for o in skills['observations']}) == len(skills['observations']), 'Duplicate skill observation')
    for o in skills['observations']:
        require(o['item_id'] in ids and o['dimension'] in DIMENSIONS and o['state'] in STATES, 'Invalid skill observation')
        require(evidence_exists(root, o['evidence']), 'Missing skill evidence')
    index = read_json(root, 'tracking/checkpoint-index.json')['checkpoints']
    require(len({c['checkpoint_id'] for c in index}) == len(index), 'Duplicate checkpoint ID')
    require(len({c['evidence_key'] for c in index}) == len(index), 'Duplicate checkpoint evidence')
    for relative, expected in views(root).items():
        require((root / relative).read_text(encoding='utf-8-sig') == expected, f'Stale derived view: {relative}; run refresh')
    return f'Validated {len(queue)} review items, {len(topics)} concepts, {len(mistakes)} mistakes, {len(review_ids)} review events.'


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('command', choices=('validate', 'refresh', 'record', 'recover', 'status', 'weekly'))
    parser.add_argument('--event', type=Path)
    parser.add_argument('--date')
    parser.add_argument('--week')
    parser.add_argument('--as-of')
    args = parser.parse_args()
    try:
        if args.command == 'validate':
            print(validate(ROOT))
        elif args.command == 'refresh':
            transaction(ROOT, views(ROOT))
            print('Refreshed compatibility views; no learning or timer events created.')
        elif args.command == 'record':
            require(args.event is not None, '--event is required')
            print('Saved.' if record(ROOT, json.loads(args.event.read_text(encoding='utf-8-sig'))) else 'Already saved; no changes.')
        elif args.command == 'recover':
            print('Recovered.' if recover(ROOT) else 'No interrupted transaction.')
        elif args.command == 'status':
            require(args.date is not None, '--date YYYY-MM-DD in IST is required')
            print(dump(status(ROOT, args.date)))
        else:
            require(args.week is not None and args.as_of is not None, '--week and --as-of are required')
            print(weekly(ROOT, args.week, args.as_of))
    except (OSError, ValueError, KeyError) as error:
        parser.exit(1, f'{error}\n')


if __name__ == '__main__':
    main()
