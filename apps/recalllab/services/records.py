"""Read-only projections of actual repository evidence."""
import csv
import importlib.util
import json
import re
from collections import defaultdict
from datetime import date, datetime, time, timedelta, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
IST = timezone(timedelta(hours=5, minutes=30), 'IST')


def now():
    return datetime.now(IST)


def is_revision(event):
    """Initial learning, application and unlabelled corrections are not revision."""
    return event.get('review_kind') == 'delayed' or event.get('practice_context') == 'revision'


def metric_events(values, metric):
    if metric == 'Revision Only':
        return values.get('revisions', [])
    return values['coding'] if metric == 'Coding Practice' else values['events']


def load_coach(root=ROOT):
    spec = importlib.util.spec_from_file_location('recalllab_coach', root / 'tracking/coach.py')
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class Records:
    def __init__(self, root=ROOT):
        self.root = Path(root).resolve()

    def json(self, path):
        return json.loads(self.path(path).read_text(encoding='utf-8-sig'))

    def csv(self, name):
        with self.path('tracking/' + name).open(encoding='utf-8-sig', newline='') as f:
            return list(csv.DictReader(f))

    def path(self, relative, notes_only=False):
        target = (self.root / relative).resolve()
        boundary = self.root / 'Notes' if notes_only else self.root
        if not target.is_relative_to(boundary.resolve()) or not target.is_file():
            raise ValueError('File is unavailable or outside the allowed folder')
        if notes_only and (target.suffix.lower() != '.md' or '.obsidian' in target.parts):
            raise ValueError('Only Markdown notes can be opened')
        return target

    def notes(self):
        return sorted(p.relative_to(self.root).as_posix() for p in (self.root / 'Notes').rglob('*.md')
                      if '.obsidian' not in p.parts)

    def events(self):
        events = []
        for row in self.csv('revision-history.csv'):
            e = json.loads(row['event_json']) if row.get('event_json') else dict(row)
            if str(e.get('question', '')).strip() and str(e.get('answer', '')).strip():
                events.append(e)
        return events

    def coverage(self, today=None):
        coach = load_coach(self.root)
        registry = self.json('tracking/topic-map.json')
        live = coach.note_revision.sync(self.root, registry, (today or now().date()).isoformat())
        state = coach.note_revision.snapshot(self.root, live, self.csv('revision-queue.csv'),
                                             self.csv('revision-history.csv'), self.json('tracking/mistakes.json'),
                                             (today or now().date()).isoformat())
        return state, live

    def activity(self, end=None):
        end = end or now().date()
        days = defaultdict(lambda: {'seconds': 0, 'events': [], 'revisions': [], 'coding': [], 'intervals': []})
        intervals = []
        for row in self.csv('study-log.csv'):
            if row['status'] != 'completed' or not row['end_time_ist']:
                continue
            start = datetime.fromisoformat(row['start_time_ist'])
            stop = datetime.fromisoformat(row['end_time_ist'])
            if start.tzinfo is None or stop.tzinfo is None or stop < start:
                continue
            start, stop = start.astimezone(IST), stop.astimezone(IST)
            intervals.append((start,stop))
            cursor = start
            while cursor < stop:
                days[cursor.date()]['intervals'].append(row)
                cursor = min(stop,datetime.combine(cursor.date()+timedelta(days=1),time.min,IST))
        merged = []
        for start, stop in sorted(intervals):
            if merged and start <= merged[-1][1]:
                merged[-1] = (merged[-1][0], max(stop,merged[-1][1]))
            else:
                merged.append((start,stop))
        for start, stop in merged:
            while start < stop:
                boundary = datetime.combine(start.date() + timedelta(days=1), time.min, IST)
                segment = min(stop, boundary)
                days[start.date()]['seconds'] += (segment - start).total_seconds()
                start = segment
        for event in self.events():
            day = date.fromisoformat(event.get('submitted_date_ist') or event['attempt_date_ist'])
            days[day]['events'].append(event)
            if is_revision(event):
                days[day]['revisions'].append(event)
            if event.get('code_submission'):
                days[day]['coding'].append(event)
        # Exactly 365 reporting dates; rectangular calendar pads outside this window.
        return {end - timedelta(days=i): days[end - timedelta(days=i)] for i in reversed(range(365))}

    def recommendations(self, events):
        registry = self.json('tracking/topic-map.json')
        topics = {t['id']: t for t in registry['topics']}
        selected = []
        ranked = sorted(reversed(events),key=lambda e: (0 if e.get('correct') is False or e.get('score') == 0 else 1 if e.get('help_used') else 2))
        for e in ranked:
            if e.get('score') == 3 and e.get('help_used') is False:
                continue
            topic = topics.get(e['item_id'])
            candidates = [topic] if topic else [t for t in topics.values() if e['item_id'] in t['exercise_ids']]
            for t in candidates:
                source_keys = {s.get('key') for s in e.get('sources',[]) if s.get('path','').startswith('Notes/')}
                focus = {'py.dict.access':('accessing items','missing'), 'py.dict.mutate':('updating','iterating'),
                         'py.records.cleaning':('copy a dictionary','conversion','fresh lists'),
                         'py.functions.basics':('fresh lists','input and return'), 'py.csv.read':('read rows with dictreader',),
                         'py.csv.write':('write dictionaries as rows','newline'), 'sql.count.nulls':('counting orders',),
                         'sql.join.preservation':('left join preservation',)}.get(t['id'],())
                words = set(re.findall(r'[a-z]{4,}',e.get('question','').lower()))
                def section_rank(s):
                    heading = s['key'].lower()
                    return (not any(term in heading for term in focus),s['key'] not in source_keys,
                            -len(words.intersection(re.findall(r'[a-z]{4,}',heading))),s['key'].count(' / '))
                sections = sorted(t.get('note_sections', []),key=section_rank)
                for section in sections:
                    key = (section['path'], section['key'])
                    if any((s['path'], s['heading']) == key for s in selected):
                        continue
                    selected.append({'path': key[0], 'heading': key[1], 'item_id': t['id'],
                                     'gap': e.get('feedback') or 'Assessment pending; inspect this section after attempting.',
                                     'evidence': e.get('evidence', e.get('attempt_id', 'Local pending submission')),
                                     'answer':e.get('answer',''), 'question':e.get('question',''),
                                     'follow_up':f'Use a different small input and reconstruct {t["name"]} without the note. Predict output and verify one edge case.',
                                     'action': 'Review this section, hide it, then reconstruct a changed example.'})
                    break
        return selected[:3]


def level(day, metric, study=(.25, .5, 1, 1.25), attempts=(1, 3, 5, 8)):
    d, values = day
    if metric == 'All Learning':
        value = values['seconds'] / ((10 if d.weekday() >= 5 else 6) * 3600)
        if value == 0:
            return 1 if values['events'] else 0
        return 1 + sum(value >= threshold for threshold in study)
    count = len(metric_events(values, metric))
    return 0 if not count else min(5, 1 + sum(count > t for t in attempts))


def metrics(activity, metric='All Learning'):
    active = [d for d, v in activity.items() if level((d, v), metric)]
    longest = run = 0
    for d in activity:
        run = run + 1 if d in active else 0
        longest = max(longest, run)
    current = 0
    d = max(activity)
    if d not in active:
        d -= timedelta(days=1)
    while d in active:
        current += 1
        d -= timedelta(days=1)
    return {'active_days': len(active), 'current_streak': current, 'longest_streak': longest,
            'hours': sum(v['seconds'] for v in activity.values()) / 3600 if metric == 'All Learning' else None,
            'attempts': sum(len(metric_events(v, metric)) for v in activity.values())}
