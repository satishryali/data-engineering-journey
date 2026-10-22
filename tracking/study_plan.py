"""Date-effective study targets and source-derived summaries. No timer writes."""
import argparse
import csv
from datetime import date, datetime, timedelta
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def config(root=ROOT):
    return json.loads((root / 'tracking/study-targets.json').read_text(encoding='utf-8'))


def target(day, settings):
    if isinstance(day, str):
        day = date.fromisoformat(day)
    policies = [p for p in settings['targets'] if p['effective_date'] <= day.isoformat()]
    if not policies:
        return 0
    policy = max(policies, key=lambda p: p['effective_date'])
    return policy['weekend_hours' if day.weekday() >= 5 else 'weekday_hours']


def days(start, end):
    while start <= end:
        yield start
        start += timedelta(days=1)


def planned(start, end, settings):
    return sum(target(d, settings) for d in days(start, end))


def summary(root, when):
    current = date.fromisoformat(when)
    settings = config(root)
    monday = current - timedelta(days=current.weekday())
    # The preparation target ends on the deadline; later status remains usable.
    end = monday + timedelta(days=6)
    deadline = date.fromisoformat(settings['preparation_deadline'])
    if monday <= deadline:
        end = min(end, deadline)
    with (root / 'tracking/study-log.csv').open(encoding='utf-8-sig', newline='') as stream:
        rows = list(csv.DictReader(stream))
    confirmed = [r for r in rows if r['status'] == 'completed' and r['study_date_ist'] <= when]
    def seconds(row):
        return (datetime.fromisoformat(row['end_time_ist']) - datetime.fromisoformat(row['start_time_ist'])).total_seconds()
    today = sum(seconds(r) for r in confirmed if r['study_date_ist'] == when) / 3600
    week = sum(seconds(r) for r in confirmed if monday.isoformat() <= r['study_date_ist'] <= end.isoformat()) / 3600
    before = sum(seconds(r) for r in confirmed if monday.isoformat() <= r['study_date_ist'] <= end.isoformat() and r['study_date_ist'] < when) / 3600
    by_topic = {}
    by_activity = {}
    for row in confirmed:
        by_topic[row['topic']] = by_topic.get(row['topic'], 0) + seconds(row) / 3600
        label = row['topic'].casefold()
        activity = 'interview' if 'interview' in label else 'revision' if 'revision' in label else 'other/unclassified'
        by_activity[activity] = by_activity.get(activity, 0) + seconds(row) / 3600
    return {'date_ist': when, 'daily_target_hours': target(current, settings),
            'weekly_target_hours': planned(monday, end, settings),
            'week_start': monday.isoformat(), 'week_end': end.isoformat(),
            'confirmed_today_hours': today, 'confirmed_week_hours': week,
            'remaining_today_hours': max(target(current, settings) - today, 0),
            'remaining_week_hours': max(planned(monday, end, settings) - week, 0),
            'closed_day_shortfall_hours': max(planned(monday, min(current - timedelta(days=1), end), settings) - before, 0),
            'confirmed_hours_by_source_topic': by_topic,
            'confirmed_hours_by_explicit_activity': by_activity,
            'preparation_deadline': settings['preparation_deadline']}


def roadmap_rows(root=ROOT):
    """The Markdown table owns the plan; CSV is a generated compatibility view."""
    text = (root / 'plan/learning-and-revision-plan.md').read_text(encoding='utf-8')
    rows = []
    for line in text.splitlines():
        cells = [c.strip() for c in line.strip().strip('|').split('|')]
        if line.startswith('| ') and cells[0].isdigit() and len(cells) == 7:
            week, start, end, focus, azure, demonstration, hours = cells
            rows.append(dict(week=week, start_date_ist=start, end_date_ist=end,
                             main_focus=focus, azure_concept=azure, demonstration=demonstration,
                             target_hours=int(hours), status='planned'))
    if len(rows) != 13:
        raise ValueError('Expected thirteen curriculum weeks')
    return rows


def activity_rows(root=ROOT):
    """Read activity allocations from the owning Markdown table, without copies."""
    text = (root / 'plan/learning-and-revision-plan.md').read_text(encoding='utf-8')
    rows = []
    for line in text.splitlines():
        cells = [c.strip() for c in line.strip().strip('|').split('|')]
        if not line.startswith('| ') or len(cells) != 4 or cells[0] == 'Total':
            continue
        try:
            weekday, weekend, weekly = map(float, cells[1:])
        except ValueError:
            continue
        rows.append({'activity': cells[0], 'weekday_hours': weekday, 'weekend_hours': weekend, 'weekly_hours': weekly})
    if len(rows) != 5 or sum(r['weekday_hours'] for r in rows) != 7 or sum(r['weekend_hours'] for r in rows) != 10 or sum(r['weekly_hours'] for r in rows) != 55:
        raise ValueError('Activity allocations do not reconcile to the new study budget')
    return rows


def refresh(root=ROOT):
    rows = roadmap_rows(root)
    with (root / 'plan/weekly-learning-plan.csv').open('w', encoding='utf-8', newline='') as stream:
        writer = csv.DictWriter(stream, fieldnames=list(rows[0]), lineterminator='\n')
        writer.writeheader()
        writer.writerows(rows)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--date', help='Actual IST reporting date, YYYY-MM-DD')
    parser.add_argument('--refresh-roadmap', action='store_true')
    args = parser.parse_args()
    if args.refresh_roadmap:
        refresh()
    if args.date:
        print(json.dumps(summary(ROOT, args.date), indent=2))
