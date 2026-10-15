"""Note coverage and revision planning; no timer or assessment writes."""

import hashlib
import json
from datetime import date, timedelta
from pathlib import Path
import re
from urllib.parse import quote


def digest(text):
    return hashlib.sha256(text.encode('utf-8')).hexdigest()


def sections(text):
    """Direct content under each heading, ignoring headings inside fenced code."""
    result, stack, body = [], [], []
    heading, fence, seen = '(preamble)', None, {}

    def emit():
        content = '\n'.join(body).strip()
        if content:
            seen[heading] = seen.get(heading, 0) + 1
            result.append({'key': heading + (f' [{seen[heading]}]' if seen[heading] > 1 else ''),
                           'heading': heading, 'content_hash': content_hash(content)})

    for line in text.splitlines():
        marker = re.match(r'^\s*(?:-\s+)?(`{3,}|~{3,})', line)
        if marker:
            token = marker[1][0]
            fence = None if fence == token else token if fence is None else fence
        match = re.match(r'^(#{1,6})\s+(.+?)\s*#*$', line) if fence is None and not marker else None
        if match:
            emit()
            level, name = len(match[1]), match[2]
            stack = [(n, h) for n, h in stack if n < level] + [(level, name)]
            heading, body = ' / '.join(h for _, h in stack), []
        else:
            body.append(line)
    emit()
    return result


def content_hash(text):
    # Ignore prose wrapping/Markdown emphasis; preserve code indentation and tokens.
    parts, prose, fence = [], [], None
    for line in text.splitlines():
        marker = re.match(r'^\s*(?:-\s+)?(`{3,}|~{3,})', line)
        if marker:
            if prose:
                parts.append(re.sub(r'\s+', ' ', ' '.join(prose)).strip())
                prose = []
            fence = None if fence else marker[1][0]
            parts.append(line.strip())
        elif fence:
            parts.append(line.rstrip())
        else:
            prose.append(re.sub(r'[*_`]', '', line).strip())
    if prose:
        parts.append(re.sub(r'\s+', ' ', ' '.join(prose)).strip())
    return digest('\n'.join(parts))


def note_files(root):
    return sorted(set(p.relative_to(root).as_posix() for p in (root / 'Notes').rglob('*')
                      if p.is_file()) | set(p.relative_to(root).as_posix()
                                           for p in (root / 'tools').glob('*/notes.md')))


def exclusion(path):
    p = Path(path)
    if '.obsidian' in p.parts:
        return 'App configuration; no learning coverage.'
    if p.suffix.lower() != '.md':
        return 'Image, asset or machine-readable view; learning is mapped from its explanation note.'
    if path.startswith('Notes/revision/'):
        return 'Revision instructions, generated view or answer-free prompts; original explanations are mapped.'
    if p.name.lower() in ('index.md', 'readme.md', 'welcome.md', 'learning-and-revision-plan.md'):
        return 'Index, vault setup or curriculum administration; no assessed lesson content.'
    return None


def inventory(root, registry):
    prior = {f['path']: f for f in registry.get('note_inventory', [])}
    result = []
    for path in note_files(root):
        old = prior.get(path, {})
        item = {'path': path, 'file_hash': hashlib.sha256((root / path).read_bytes()).hexdigest()}
        reason = exclusion(path) or (old.get('exclusion_reason') if old.get('file_hash') == item['file_hash'] else None)
        if reason:
            item['exclusion_reason'] = reason
            if exclusion(path):
                item.pop('file_hash')  # Generated views must not hash themselves.
        else:
            previous = {s['key']: s for s in old.get('sections', [])}
            item['sections'] = []
            for section in sections((root / path).read_text(encoding='utf-8-sig')):
                saved = previous.get(section['key'], {})
                section.update({k: saved[k] for k in ('topic_ids', 'exclusion_reason') if k in saved})
                if saved and saved['content_hash'] != section['content_hash']:
                    section['changed'] = True
                elif saved.get('changed'):
                    section['changed'] = True
                item['sections'].append(section)
            removed = set(previous) - {s['key'] for s in item['sections']}
            if removed:
                item['removed_sections'] = sorted(removed)
            elif old.get('removed_sections'):
                item['removed_sections'] = old['removed_sections']
        result.append(item)
    return result


def sync(root, registry, when):
    """Discover gaps, flag affected concepts, preserve IDs, history and review dates."""
    date.fromisoformat(when)
    old_files = {f['path']: f for f in registry.get('note_inventory', [])}
    found = inventory(root, registry)
    by_id = {t['id']: t for t in registry['topics']}
    for item in found:
        old = old_files.get(item['path'], {})
        old_sections = {s['key']: s for s in old.get('sections', [])}
        for section in item.get('sections', []):
            if section.get('changed'):
                for ident in section.get('topic_ids', []):
                    topic = by_id[ident]
                    topic['needs_reassessment'] = True
                    history = topic.setdefault('content_changes', [])
                    change = {'path': item['path'], 'section': section['key'],
                              'prior_hash': old_sections.get(section['key'], {}).get('content_hash'),
                              'content_hash': section['content_hash'], 'detected_date_ist': when}
                    if not any(c.get('content_hash') == change['content_hash'] and c.get('section') == change['section'] for c in history):
                        history.append(change)
    registry['note_inventory'] = found
    registry['inventory_date_ist'] = when
    return registry


def check(root, registry):
    topics = {t['id']: t for t in registry['topics']}
    stored = {f['path']: f for f in registry.get('note_inventory', [])}
    if set(note_files(root)) != set(stored):
        raise ValueError('Notes inventory changed; run notes-sync and map new learning sections')
    for actual in inventory(root, registry):
        saved = stored[actual['path']]
        if actual != saved:
            raise ValueError(f'Stale notes inventory: {actual["path"]}; run notes-sync')
        for section in actual.get('sections', []):
            ids = section.get('topic_ids', [])
            if bool(ids) == bool(section.get('exclusion_reason')):
                raise ValueError(f'Map or explain exclusion of section: {actual["path"]} / {section["key"]}')
            if len(ids) != len(set(ids)) or any(i not in topics for i in ids):
                raise ValueError('Invalid or duplicate section topic ID')
    names = [t['name'].casefold().strip() for t in topics.values()]
    if len(names) != len(set(names)):
        raise ValueError('Duplicate concept names; reuse the existing topic ID')
    for topic in topics.values():
        if topic.get('initial_assessment_date_ist'):
            date.fromisoformat(topic['initial_assessment_date_ist'])
        for ref in topic.get('note_sections', []):
            source = stored.get(ref['path'], {})
            matches = [s for s in source.get('sections', []) if s['key'] == ref['key']]
            if not matches or topic['id'] not in matches[0].get('topic_ids', []):
                raise ValueError(f'Broken section link for {topic["id"]}')


def snapshot(root, registry, queue, history, mistakes, when):
    date.fromisoformat(when)
    events = [json.loads(r['event_json']) for r in history if r.get('event_json')]
    events = [e for e in events if e['attempt_date_ist'] <= when]
    by_id = {q['item_id']: q for q in queue}
    items = []
    for topic in registry['topics']:
        ident = topic['id']
        actual = [e for e in events if e['item_id'] == ident]
        scored = [e for e in actual if e.get('score') is not None and e['review_kind'] != 'immediate_correction']
        independent = lambda e: (e.get('result') == 'independent' and e.get('help_used') is False
                                 and e.get('notes_used') is False and e.get('hints_used') == 0 and e.get('score') in (2, 3))
        latest = scored[-1] if scored else None
        state = 'Unassessed'
        if latest:
            state = ('Demonstrated on delayed review' if latest['review_kind'] == 'delayed' else 'Applied independently') if independent(latest) else 'Learning with help'
        row = by_id[ident]
        items.append({'id': ident, 'name': topic['name'], 'state': state,
                      'initial_assessment_date_ist': topic.get('initial_assessment_date_ist'),
                      'last_actual_review': actual[-1]['attempt_date_ist'] if actual else None,
                      'next_review_date': row['next_review_date_ist'] or None,
                      'delayed_practised': any(e['review_kind'] == 'delayed' for e in actual),
                      'last_independent_application': next((e['attempt_date_ist'] for e in reversed(scored) if independent(e)), None),
                      'evidence': actual[-1].get('evidence') if actual else None,
                      'help_used': actual[-1].get('help_used') if actual else None,
                      'notes_used': actual[-1].get('notes_used') if actual else None,
                      'hints_used': actual[-1].get('hints_used') if actual else None,
                      'prerequisites': topic['prerequisites'], 'exercise_ids': topic['exercise_ids'],
                      'needs_reassessment': topic.get('needs_reassessment', False),
                      'note_sections': topic.get('note_sections', []),
                      'mistakes': [m['mistake_id'] for m in mistakes['mistakes'] if ident in m['topic_ids'] and m['status'] != 'verified_on_delayed_independent_practice']})
    files = inventory(root, registry)
    all_sections = [(f['path'], s) for f in files for s in f.get('sections', [])]
    gaps = [f'{p} / {s["key"]}' for p, s in all_sections if not s.get('topic_ids') and not s.get('exclusion_reason')]
    stored_paths = {f['path'] for f in registry.get('note_inventory', [])}
    gaps.extend('New file: ' + f['path'] for f in files if f['path'] not in stored_paths and not f.get('exclusion_reason'))
    gaps.extend('Removed source: ' + p for p in stored_paths - {f['path'] for f in files})
    gaps.extend(f'Removed section: {f["path"]} / {key}' for f in registry.get('note_inventory', []) for key in f.get('removed_sections', []))
    neglected = [t['id'] for t in items if (t['state'] == 'Unassessed' and t['initial_assessment_date_ist'] and t['initial_assessment_date_ist'] < when)
                 or (t['last_independent_application'] and (date.fromisoformat(when) - date.fromisoformat(t['last_independent_application'])).days >= 30)]
    return {'date_ist': when, 'topics': items, 'gaps': gaps, 'neglected_topics': neglected,
            'coverage': {'learning_sections_mapped': sum(bool(s.get('topic_ids')) for _, s in all_sections),
                         'sections_excluded': sum(bool(s.get('exclusion_reason')) for _, s in all_sections),
                         'topics_total': len(items), 'topics_assessed': sum(t['state'] != 'Unassessed' for t in items),
                         'topics_practised_on_delayed_review': sum(t['delayed_practised'] for t in items),
                         'topics_needing_help': sum(t['state'] == 'Learning with help' for t in items)}}


def selection(state, queue, minutes=15):
    """At most two targets; one diagnostic slot, with prerequisites and overlap visible."""
    when = state['date_ist']
    topics = {t['id']: t for t in state['topics']}
    due = [q for q in queue if q['next_review_date_ist'] and q['next_review_date_ist'] <= when]
    def rank(q):
        topic = topics.get(q['item_id'], {})
        return (q['last_result'] not in ('needs_guidance', 'assisted'), q['next_review_date_ist'],
                -len(topic.get('mistakes', [])), topic.get('last_independent_application') or '', q['item_id'])
    due.sort(key=rank)
    selected = [{'id': q['item_id'], 'kind': 'follow-up', 'minutes': min(10, minutes)} for q in due[:1]]
    for target in selected:
        related = [t for t in state['topics'] if target['id'] in t['exercise_ids']]
        prerequisites = sorted({p for t in related for p in t['prerequisites'] if topics[p]['state'] in ('Unassessed', 'Learning with help')},
                               key=lambda p: (len(topics[p]['prerequisites']), p))
        if prerequisites:
            target.update(id=prerequisites[0], kind='prerequisite check; teach if needed',
                          deferred_broad_exercise=target['id'], minutes=min(10, minutes))
    candidates = [t for t in state['topics'] if t['state'] == 'Unassessed' and t['initial_assessment_date_ist'] and t['initial_assessment_date_ist'] <= when]
    candidates.sort(key=lambda t: (len(t['prerequisites']), -len(t['mistakes']), t['initial_assessment_date_ist'], t['id']))
    initial_slot_used = any(topics.get(s['id'], {}).get('state') == 'Unassessed' for s in selected)
    if (minutes >= 15 or not selected) and not initial_slot_used:
        for topic in candidates:
            if any(s['id'] == topic['id'] for s in selected):
                continue
            if any(topics[p]['state'] in ('Unassessed', 'Learning with help') for p in topic['prerequisites']):
                continue
            # A broad follow-up can assess this concept too, but must record its own evidence.
            overlap = next((s for s in selected if s['id'] in topic['exercise_ids']), None)
            if overlap:
                overlap['concept_to_assess_if_demonstrated'] = topic['id']
                break
            selected.append({'id': topic['id'], 'kind': 'initial assessment', 'minutes': min(5, minutes),
                             'prerequisites_to_check': topic['prerequisites']})
            break
    return selected


def render(state, registry, queue):
    when, counts = state['date_ist'], state['coverage']
    lines = ['# Revision plan (generated)', '', f'As of {when} IST. Refresh at revision planning or checkpoint boundaries.',
             'Source: topic-map + revision queue/history + mistakes. This plan does not record an attempt.', '',
             '## Coverage', '', '| Count | Meaning |', '| ---: | --- |']
    for key, value in counts.items():
        lines.append(f'| {value} | {key.replace("_", " ")} |')
    lines += ['', 'Assessed = a scored, non-immediate concept assessment. Delayed practice = an actual answered delayed event;',
              'it can be incorrect or assisted. Neither count means permanent retention. Broad exercise results stay separate.', '',
              '## Due today', '']
    def rows(values):
        return [f'- **{q["item_id"]}**: {q["skill"]}; due {q["next_review_date_ist"]}; last result {q["last_result"]}.' for q in values] or ['- None.']
    lines += rows(q for q in queue if q['next_review_date_ist'] == when)
    lines += ['', '## Overdue', ''] + rows(q for q in queue if q['next_review_date_ist'] and q['next_review_date_ist'] < when)
    lines += ['', '## Upcoming reviews', ''] + rows(sorted((q for q in queue if q['next_review_date_ist'] > when), key=lambda q: q['next_review_date_ist']))
    lines += ['', '## Awaiting initial assessment', '', 'Dates below are adjustable planning slots, not completed reviews or overdue retention.', '',
              '| Topic | Initial slot | Prerequisites |', '| --- | --- | --- |']
    for t in sorted(state['topics'], key=lambda t: (t['initial_assessment_date_ist'] or '9999', t['id'])):
        if t['state'] == 'Unassessed':
            lines.append(f'| {t["id"]}: {t["name"]} | {t["initial_assessment_date_ist"] or "Plan needed"} | {", ".join(t["prerequisites"]) or "None"} |')
    lines += ['', '## Important weak topics', '']
    lines += [f'- Exercise {q["item_id"]}: {q["last_result"]}. Historical exercise evidence is separate from concept assessment counts.'
              for q in queue if q['item_id'] not in {t['id'] for t in state['topics']} and q['last_result'] in ('needs_guidance', 'assisted')]
    weak = [t for t in state['topics'] if t['mistakes'] or t['state'] == 'Learning with help']
    lines += [f'- {t["id"]}: {t["state"]}; linked mistakes {", ".join(t["mistakes"]) or "none"}.' for t in weak] or ['- No observed gaps recorded.']
    lines += ['', '## Coverage gaps', '']
    lines += ['- ' + gap for gap in state['gaps']] or ['- Every included learning section has a topic mapping.']
    lines += ['- Neglected topics: ' + (', '.join(state['neglected_topics']) or 'none under the current rules (missed initial slots or 30 days since independent application).')]
    lines += ['- Reassessment flags: ' + (', '.join(t['id'] for t in state['topics'] if t['needs_reassessment']) or 'none.')]
    lines += ['', '## Manageable session', '', 'Default: 15–20 minutes; one meaningful task at a time, at most one new diagnostic concept.',
              'Check prerequisites first. Teach missing understanding before retention practice. No timer starts from planning.']
    selected = selection(state, queue)
    lines += [f'- {s["id"]}: {s["kind"]}, about {s["minutes"]} minutes. ' + (f'Check concept {s["concept_to_assess_if_demonstrated"]} in the same task; no automatic score transfer.' if s.get('concept_to_assess_if_demonstrated') else '') for s in selected]
    if not selected:
        lines.append('- No eligible review is due today. Keep the exact pending learning task in progress/current.md; add a short due follow-up in the next suitable session.')
    awaiting = sum(t['state'] == 'Unassessed' for t in state['topics'])
    lines += [f'- {awaiting} topics await assessment. One diagnostic per suitable session needs at least {awaiting} sessions; new notes can extend this. Replan missed slots without restarting.', '',
              '## Topic evidence', '', '| Topic | State | Last actual review | Next review | Evidence / help |', '| --- | --- | --- | --- | --- |']
    for t in state['topics']:
        lines.append(f'| {t["id"]} | {t["state"]} | {t["last_actual_review"] or "None"} | {t["next_review_date"] or "None"} | {t["evidence"] or "No concept assessment"}; help={t["help_used"]}, notes={t["notes_used"]}, hints={t["hints_used"]} |')
    lines += ['', '## Source sections and exclusions', '', 'A section is direct content under a Markdown heading (or a preamble); code-fence headings are ignored.',
              'Related sections share topic IDs. Empty container headings are not counted.', '']
    for item in registry.get('note_inventory', []):
        link = quote('../../' + item['path'], safe='/')
        lines.append(f'- [{item["path"]}]({link})' + (': ' + item['exclusion_reason'] if item.get('exclusion_reason') else ''))
        for section in item.get('sections', []):
            label = ', '.join(section.get('topic_ids', [])) or section.get('exclusion_reason', 'MAPPING NEEDED')
            lines.append(f'  - {section["heading"]}: {label}')
    return '\n'.join(lines) + '\n'
