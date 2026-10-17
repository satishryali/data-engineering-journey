"""Compact dashboard, projected only from real records and local submitted work."""
from datetime import timedelta
from html import escape
from urllib.parse import urlencode
from components.calendar import heatmap
from services.questions import daily_queue
from services.records import metrics, is_revision
from services.routing import app_url, PAGES


PATHS = {
    'book': '<path d="M3 4c3-1 6-1 9 1v15c-3-2-6-2-9-1zM21 4c-3-1-6-1-9 1v15c3-2 6-2 9-1z"/>',
    'calendar': '<rect x="3" y="5" width="18" height="16" rx="2"/><path d="M7 3v4m10-4v4M3 11h18"/>',
    'target': '<circle cx="11" cy="13" r="8"/><circle cx="11" cy="13" r="4"/><path d="m11 13 9-10m-4 0h4v4"/>',
    'code': '<path d="m8 6-6 6 6 6m8-12 6 6-6 6m-3-15-2 18"/>',
    'clock': '<circle cx="12" cy="12" r="9"/><path d="M12 6v6l4 2"/>',
    'chart': '<path d="M4 21V11m5 10V4m6 17V8m5 13V2"/>',
    'trophy': '<path d="M7 3h10v7a5 5 0 0 1-10 0zM7 5H3v3c0 4 4 4 4 4m10-7h4v3c0 4-4 4-4 4m-5 3v6m-4 0h8"/>',
    'flame': '<path d="M13 2c1 5-4 6-2 10 2-1 3-3 3-4 4 3 6 6 4 10a7 7 0 0 1-12 0C2 12 9 8 8 5c3 0 4 4 5-3z"/>',
    'home': '<path d="m3 10 9-7 9 7v11h-6v-7H9v7H3z"/>',
    'play': '<path d="m8 4 12 8-12 8z"/>',
}


def icon(name, color=''):
    return f'<span class="rl-icon {color}" aria-hidden="true"><svg viewBox="0 0 24 24">{PATHS.get(name, PATHS["book"])}</svg></span>'


def link(page, **args):
    return escape(app_url(page, **args), quote=True)


def brand():
    return f'<div class="rl-brand">{icon("book")}<div>RecallLab<small>Data Engineering Journey</small></div></div>'


def topbar(today):
    menu = ''.join(f'<a target="_self" href="{link(p)}">{escape(p)}</a>' for p in PAGES)
    return f'<div class="rl-topbar"><span>RecallLab workspace</span><div class="rl-profile"><span class="rl-date">{today:%a, %d %b %Y} · IST</span><span class="rl-avatar">S</span><span>Satish</span></div></div><details class="rl-mobile-nav"><summary>☰ Navigate RecallLab</summary><nav>{menu}</nav></details>'


def dashboard(records, journal, today, settings):
    activity = records.activity(today)
    stats = metrics(activity)
    events = records.events()
    # A pending attempt and its canonical replay are one actual submission.
    combined = {e.get('review_id', e.get('attempt_id', str(i))): e for i, e in enumerate(events)}
    combined.update({e['review_id']: e for e in journal.effective_attempts()})
    all_events = list(combined.values())
    local_today = [e for e in all_events if e['attempt_date_ist'] == str(today)]
    queue = daily_queue(records, settings['session_minutes'], today)
    topics = {t['id']: t for t in records.json('tracking/topic-map.json')['topics']}
    rows = {r['item_id']: r for r in records.csv('revision-queue.csv')}
    due_today = sum(r['next_review_date_ist']==str(today) for r in rows.values())
    overdue = sum(bool(r['next_review_date_ist']) and r['next_review_date_ist']<str(today) for r in rows.values())
    weak_count = sum(r['item_id'] in topics and r['last_result'] in ('assisted','needs_guidance') for r in rows.values())
    notes = records.recommendations(all_events[-10:])
    start = today - timedelta(days=today.weekday())
    week_events = [e for e in all_events if str(start) <= e['attempt_date_ist'] <= str(today)]
    objective = [e for e in week_events if is_revision(e) and type(e.get('correct')) is bool]
    accuracy = f'{100*sum(e["correct"] for e in objective)/len(objective):.0f}%' if objective else 'Unassessed'
    coded = [e for e in local_today if e.get('code_submission')]
    tested = [e for e in coded if e.get('test_evidence') is not None]
    passed = sum(bool(e['test_evidence'].get('passed')) for e in tested)
    complete = sum(any(e['item_id'] == q['id'] for e in local_today) for q in queue)
    pct = round(100 * complete / len(queue)) if queue else 0
    stat_cells = ''.join(f'<div class="rl-stat">{icon(i,c)}<div><strong>{v}</strong><small>{label}</small></div></div>' for i,c,v,label in [
        ('calendar','rl-blue',str(stats['active_days']),'Active days'),
        ('flame','rl-amber',f'{stats["current_streak"]} days','Current streak'),
        ('trophy','rl-amber',f'{stats["longest_streak"]} days','Longest streak'),
        ('clock','rl-green',f'{stats["hours"]:.1f} hrs','Confirmed study time')])
    calendar = heatmap(activity, 'All Learning', settings['study_thresholds'], settings['attempt_thresholds'])
    summary = f'''<div class="rl-summary">
    <a class="rl-card blue" target="_self" href="{link("Today's Session")}"><div class="rl-cardtitle">{icon('home','rl-blue')}Today's Progress</div><div class="rl-progressvalue"><div class="rl-ring" style="--progress:{pct}%"><span>{pct}%</span></div><div><div class="rl-cardvalue">{complete} / {len(queue)}</div><div class="rl-cardfoot">suggested topics attempted</div></div></div></a>
    <a class="rl-card green" target="_self" href="{link('Progress & Analytics')}"><div class="rl-cardtitle">{icon('target','rl-green')}Revision Accuracy</div><div class="rl-cardvalue">{accuracy}</div><div class="rl-cardfoot">This week · verified outputs only</div></a>
    <a class="rl-card purple" target="_self" href="{link('Coding Challenges')}"><div class="rl-cardtitle">{icon('code','rl-purple')}Coding Challenges</div><div class="rl-cardvalue">{passed} / {len(tested)}</div><div class="rl-cardfoot">tested submissions passed today</div></a>
    <a class="rl-card amber" target="_self" href="{link('Notes Browser',recommended='1')}"><div class="rl-cardtitle">{icon('book','rl-amber')}Notes to Review</div><div class="rl-cardvalue">{len(notes)}</div><div class="rl-cardfoot">specific sections from your evidence &nbsp; ↗</div></a></div>'''
    tasks = []
    for i, target in enumerate(queue):
        ident = target['id']
        title = topics.get(ident, {}).get('name', rows.get(ident, {}).get('skill', ident))
        done = any(e['item_id'] == ident for e in local_today)
        tasks.append(f'<div class="rl-task"><span class="rl-number">{"✓" if done else i+1}</span><div><strong>{escape(title)}</strong><small>{escape(target["kind"])}</small></div><span class="rl-chip">{"SQL" if ident.startswith(("sql", "SQL")) else "Python" if ident.startswith(("py", "PY")) else "Recall"}</span><a class="rl-cta" target="_self" href="{link("Today\u0027s Session",item=ident)}">{"Retry" if done else "Start"}</a></div>')
    if not tasks:
        tasks = ['<div class="rl-empty">No due task selected. Choose a concept from the Question Bank.</div>']
    coding_id = 'sql-join' if queue and queue[0]['id'].startswith(('sql','SQL')) else 'clean-records'
    task_panel = f'''<section class="rl-panel"><div class="rl-panelhead"><div><div class="rl-title">{icon('target','rl-red')}Today's Revision</div><div class="rl-sub">{due_today} due today · {overdue} overdue · {weak_count} concepts need help</div></div><div><span class="rl-duration">◷ ~{settings['session_minutes']} min</span><a class="rl-cta" target="_self" href="{link("Today's Session")}">{icon('play')}Start Today's Revision</a></div></div>{''.join(tasks)}<div class="rl-caption">A bounded mixed session: retrieve, debug, code, then save. <a class="rl-view" href="{link('Coding Challenges',challenge=coding_id)}" target="_self">Suggested coding challenge ↗</a></div></section>'''
    recent = []
    for event in reversed(all_events[-5:]):
        result = event.get('result', 'unknown')
        result = result if result in ('independent','assisted','needs_guidance','unknown') else 'unknown'
        title = topics.get(event['item_id'], {}).get('name', rows.get(event['item_id'], {}).get('skill',event['item_id']))
        recent.append(f'<tr><td>{escape(event["attempt_date_ist"][5:])}</td><td>{escape(title)}</td><td>{"Coding" if event.get("code_submission") else assessment_label(event)}</td><td><span class="rl-badge {result}">{escape(result.replace("_"," "))}</span></td></tr>')
    recent_panel = f'<section class="rl-panel"><div class="rl-panelhead"><span class="rl-title">{icon("clock","rl-blue")}Recent Activity</span><a class="rl-view" href="{link("Revision Calendar")}" target="_self">View all</a></div><table class="rl-table"><thead><tr><th>Date</th><th>Topic</th><th>Type</th><th>Result</th></tr></thead><tbody>{"".join(recent)}</tbody></table>{"" if recent else "<div class=rl-empty>No answered reviews recorded yet.</div>"}</section>'
    note_rows = ''.join(f'<div class="rl-note">{icon("book")}<div><strong>{escape(PathLabel(n["path"]))}</strong><small title="{escape(n["heading"])}">Section: {escape(n["heading"])}</small></div><a class="rl-review" target="_self" href="{link("Notes Browser",note=n["path"],heading=n["heading"])}">Review</a></div>' for n in notes)
    note_panel = f'<section class="rl-panel"><div class="rl-panelhead"><div><span class="rl-title">{icon("book","rl-purple")}Recommended Notes</span><div class="rl-sub">Based on actual attempts and recorded help.</div></div><a class="rl-view" target="_self" href="{link("Notes Browser",recommended="1")}">View all</a></div>{note_rows or "<div class=rl-empty>No mapped recommendations yet.</div>"}</section>'
    weak = [r for r in rows.values() if r['last_result'] in ('assisted','needs_guidance')]
    weak.sort(key=lambda r:(r['last_result']!='needs_guidance',r['next_review_date_ist'] or '9999'))
    focus = []
    for row in weak[:4]:
        count = sum(m['recurrence_count'] for m in records.json('tracking/mistakes.json')['mistakes'] if row['item_id'] in m['linked_review_items'])
        focus.append(f'<div class="rl-focus">{icon("book","rl-amber")}<div><strong>{escape(row["skill"])}</strong><small>{count} observed mistake attempts · {escape(row["last_result"].replace("_"," "))}</small></div><span class="rl-badge assisted">Review</span></div>')
    focus_panel = f'<section class="rl-panel"><div class="rl-panelhead"><div><span class="rl-title">{icon("target","rl-red")}Focus Areas</span><div class="rl-sub">Evidence of help needed, separate from activity.</div></div><a class="rl-view" href="{link("Mistakes & Weak Topics")}" target="_self">View all</a></div>{"".join(focus) or "<div class=rl-empty>No assessed weak topics yet.</div>"}</section>'
    days = [(start+timedelta(days=i),activity.get(start+timedelta(days=i),{}).get('seconds',0)/3600) for i in range(7)]
    peak = max(1,max(h for _,h in days))
    bars = ''.join(f'<div class="rl-barcol" title="{d}: {h:.2f} confirmed hours"><div class="rl-bar {"empty" if not h else ""}" style="height:{max(2,round(65*h/peak))}px"></div><span>{d:%a}</span></div>' for d,h in days)
    hours = sum(h for _,h in days)
    assessed = [e for e in week_events if is_revision(e) and e.get('score') is not None]
    independent = f'{100*sum(e.get("result")=="independent" and e["score"]>=2 for e in assessed)/len(assessed):.0f}%' if assessed else '—'
    week_panel = f'<section class="rl-panel"><div class="rl-title">{icon("chart","rl-blue")}This Week</div><div class="rl-weeknumbers"><div><small>Answers</small><strong>{len(week_events)}</strong></div><div><small>Independent revision</small><strong>{independent}</strong></div><div><small>Study time</small><strong>{hours:.1f}<small> hrs</small></strong></div></div><div class="rl-bars">{bars}</div><div class="rl-caption">Confirmed closed intervals · breaks excluded.<br>Unknown outcomes never become an accuracy score.</div></section>'
    return f'''<div class="rl-dashboard"><div class="rl-welcome"><div><h1>Welcome back, Satish!</h1><p>Keep going. Consistent revision builds long-term memory.</p></div><div class="rl-quote">“Small consistent efforts create big results.”<small>Data Engineering Journey</small></div></div><div class="rl-activity"><section class="rl-panel"><div class="rl-panelhead"><div class="rl-title">{icon('calendar','rl-green')}Study &amp; Learning Activity</div><a class="rl-view" target="_self" href="{link('Revision Calendar')}">Explore calendar ↗</a></div>{calendar}<div class="rl-caption">365 days · confirmed study + learning assessments · deepest green ≥125% of daily study target</div></section><section class="rl-panel rl-stats">{stat_cells}</section></div>{summary}<div class="rl-main"><div class="rl-left">{task_panel}<div class="rl-bottom">{recent_panel}{note_panel}</div></div><div class="rl-right">{focus_panel}{week_panel}</div></div></div>'''


def assessment_label(event):
    if is_revision(event):
        return 'Revision'
    return {'initial_learning': 'Initial learning', 'diagnostic': 'Diagnostic',
            'application': 'Application', 'immediate_correction': 'Correction'}.get(event.get('review_kind'), 'Learning')


def PathLabel(path):
    return path.removeprefix('Notes/').removesuffix('.md')
