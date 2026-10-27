"""Revision-first dashboard, projected only from real records and submitted work."""
from datetime import timedelta
from html import escape
from components.calendar import heatmap
from services.questions import daily_queue
from services.records import metrics, is_revision
from services.routing import app_url, PAGES


PATHS = {
    'book': '<path d="M3 4c3-1 6-1 9 1v15c-3-2-6-2-9-1zM21 4c-3-1-6-1-9 1v15c3-2 6-2 9-1z"/>',
    'calendar': '<rect x="3" y="5" width="18" height="16" rx="2"/><path d="M7 3v4m10-4v4M3 11h18"/>',
    'target': '<circle cx="12" cy="12" r="9"/><circle cx="12" cy="12" r="4"/><path d="m12 12 8-9"/>',
    'code': '<path d="m8 6-6 6 6 6m8-12 6 6-6 6m-3-15-2 18"/>',
    'clock': '<circle cx="12" cy="12" r="9"/><path d="M12 6v6l4 2"/>',
    'chart': '<path d="M4 21V11m5 10V4m6 17V8m5 13V2"/>',
    'trophy': '<path d="M7 3h10v7a5 5 0 0 1-10 0zM7 5H3v3c0 4 4 4 4 4m10-7h4v3c0 4-4 4-4 4m-5 3v6m-4 0h8"/>',
    'flame': '<path d="M13 2c1 5-4 6-2 10 2-1 3-3 3-4 4 3 6 6 4 10a7 7 0 0 1-12 0C2 12 9 8 8 5c3 0 4 4 5-3z"/>',
    'home': '<path d="m3 10 9-7 9 7v11h-6v-7H9v7H3z"/>',
    'play': '<path d="m9 5 10 7-10 7z"/>',
    'arrow': '<path d="M4 12h16m-6-6 6 6-6 6"/>',
    'check': '<path d="m5 12 4 4L19 6"/>',
}


def icon(name, color=''):
    return f'<span class="rl-icon {color}" aria-hidden="true"><svg viewBox="0 0 24 24">{PATHS.get(name, PATHS["book"])}</svg></span>'


def link(page, **args):
    return escape(app_url(page, **args), quote=True)


def brand():
    return f'<div class="rl-brand">{icon("book")}<div>RecallLab<small>Your learning workspace</small></div></div>'


def topbar(today):
    menu = ''.join(f'<a target="_self" href="{link(p)}">{escape(p)}</a>' for p in PAGES)
    return f'<div class="rl-topbar"><span>Personal workspace <span class="rl-topbar-separator">/</span> Data engineering</span><div class="rl-profile"><span class="rl-date">{today:%a, %d %b %Y} · IST</span></div></div><details class="rl-mobile-nav"><summary>Navigate RecallLab</summary><nav>{menu}</nav></details>'


def dashboard(records, journal, today, settings):
    activity = records.activity(today)
    stats = metrics(activity)
    events = records.events()
    # Canonical replay and a pending local attempt represent one submission.
    combined = {e.get('review_id', e.get('attempt_id', str(i))): e for i, e in enumerate(events)}
    combined.update({e['review_id']: e for e in journal.effective_attempts()})
    all_events = sorted(combined.values(), key=lambda e: e['attempt_date_ist'])
    local_today = [e for e in all_events if e['attempt_date_ist'] == str(today)]
    queue = daily_queue(records, settings['session_minutes'], today)
    topics = {t['id']: t for t in records.json('tracking/topic-map.json')['topics']}
    rows = {r['item_id']: r for r in records.csv('revision-queue.csv')}
    due_today = sum(r['next_review_date_ist'] == str(today) for r in rows.values())
    overdue = sum(bool(r['next_review_date_ist']) and r['next_review_date_ist'] < str(today) for r in rows.values())
    notes = records.recommendations(all_events[-10:])
    start = today - timedelta(days=today.weekday())
    week_events = [e for e in all_events if str(start) <= e['attempt_date_ist'] <= str(today)]
    objective = [e for e in week_events if is_revision(e) and type(e.get('correct')) is bool]
    accuracy = f'{100 * sum(e["correct"] for e in objective) / len(objective):.0f}%' if objective else 'Unassessed'
    complete = sum(any(e['item_id'] == q['id'] for e in local_today) for q in queue)
    remaining = len(queue) - complete
    hours = sum(activity.get(start + timedelta(days=i), {}).get('seconds', 0) for i in range(7)) / 3600
    hero = f'''<section class="rl-session-hero" aria-label="Today's revision">
        <div class="rl-hero-copy"><div class="rl-eyebrow">YOUR DAILY PRACTICE</div><h1>A little recall.<br>A stronger foundation.</h1>
        <p>Your next session is ready. Revisit a few concepts, test what you remember, and build from there.</p>
        <a class="rl-primary-action" target="_self" href="{link("Today's Session")}">{icon('play')}Start Today's Revision{icon('arrow')}</a>
        <div class="rl-hero-meta">{icon('clock')}About {settings['session_minutes']} min<span>·</span>{len(queue)} selected topics<span>·</span>At your pace</div></div>
        <div class="rl-session-preview"><div class="rl-eyebrow">TODAY'S FOCUS</div><div class="rl-session-count">{remaining}<span>topics to revisit</span></div><div class="rl-session-rule"></div><p>{complete} of {len(queue)} selected topics attempted today</p><a class="rl-text-link" target="_self" href="{link("Today's Session")}">View your session {icon('arrow')}</a></div>
    </section>'''
    metric_cells = ''.join(f'<a class="rl-overview-cell" target="_self" href="{link(page)}"><small>{label}</small><strong>{value}</strong><span>{detail}</span></a>' for page, label, value, detail in [
        ('Progress & Analytics', 'THIS WEEK', f'{len(week_events)}', 'submitted attempts'),
        ('Progress & Analytics', 'REVISION ACCURACY', accuracy, f'{len(objective)} verified outputs this week'),
        ('Revision Calendar', 'CONFIRMED STUDY', f'{hours:.1f} hrs', 'this week · breaks excluded'),
        ('Revision Calendar', 'CURRENT STREAK', f'{stats["current_streak"]} days', 'recorded learning activity'),
    ])
    tasks = []
    for i, target in enumerate(queue):
        ident = target['id']
        title = topics.get(ident, {}).get('name', rows.get(ident, {}).get('skill', ident))
        done = any(e['item_id'] == ident for e in local_today)
        category = 'SQL' if ident.lower().startswith('sql') else 'Python' if ident.lower().startswith('py') else 'Recall'
        marker = icon('check') if done else f'{i + 1:02}'
        tasks.append(f'<a class="rl-queue-row" target="_self" href="{link("Today\u0027s Session", item=ident)}"><span class="rl-queue-number {"rl-is-done" if done else ""}">{marker}</span><div class="rl-queue-topic"><strong>{escape(title)}</strong><small>{escape(target["kind"].replace("_", " "))}</small></div><span class="rl-topic-tag">{category}</span><span class="rl-queue-action">{"Retry" if done else "Practise"}{icon("arrow")}</span></a>')
    task_panel = f'''<section class="rl-panel rl-queue-panel"><div class="rl-section-head"><div><div class="rl-eyebrow">A MANAGEABLE NEXT STEP</div><h2>Your revision queue <span>{len(queue)}</span></h2></div><a class="rl-text-link" target="_self" href="{link('Question Bank')}">Question bank {icon('arrow')}</a></div><p class="rl-section-description">A small selection for this session. You can leave the rest for another day.</p>{''.join(tasks) or '<div class="rl-empty">No topics selected. Browse the question bank to choose your next concept.</div>'}<div class="rl-queue-footer"><span>{due_today} due today · {overdue} earlier scheduled reviews</span><span>Attempt first. Check notes after.</span></div></section>'''
    note_rows = ''.join(f'<a class="rl-note-row" target="_self" href="{link("Notes Browser", note=n["path"], heading=n["heading"])}">{icon("book")}<div><strong>{escape(PathLabel(n["path"]))}</strong><small>{escape(n["heading"])}</small></div>{icon("arrow")}</a>' for n in notes[:3])
    note_panel = f'<section class="rl-panel rl-notes-panel"><div class="rl-section-head"><h2>Back to your notes</h2>{icon("book")}</div><p class="rl-section-description">Useful sections based on your recent attempts.</p>{note_rows or "<div class=rl-empty>Recommendations appear when attempts link to your notes.</div>"}<a class="rl-text-link rl-panel-link" target="_self" href="{link("Notes Browser", recommended="1")}">Browse recommended notes {icon("arrow")}</a></section>'
    weak = sorted((r for r in rows.values() if r['last_result'] in ('assisted', 'needs_guidance')), key=lambda r: (r['last_result'] != 'needs_guidance', r['next_review_date_ist'] or '9999'))
    focus_rows = ''.join(f'<a class="rl-focus-row" target="_self" href="{link("Mistakes & Weak Topics")}"><strong>{escape(row["skill"])}</strong><small>{"Needs guidance" if row["last_result"] == "needs_guidance" else "Previously assisted"}</small></a>' for row in weak[:2])
    focus_panel = f'<section class="rl-panel rl-focus-panel"><div class="rl-section-head"><h2>Room to grow</h2>{icon("target")}</div><p class="rl-section-description">Where a little extra practice could help.</p>{focus_rows or "<div class=rl-empty>No assessed weak topics recorded yet.</div>"}<a class="rl-text-link rl-panel-link" target="_self" href="{link("Mistakes & Weak Topics")}">Explore focus areas {icon("arrow")}</a></section>'
    recent = []
    for event in reversed(all_events[-4:]):
        result = event.get('result', 'unknown')
        result = result if result in ('independent', 'assisted', 'needs_guidance', 'unknown') else 'unknown'
        title = topics.get(event['item_id'], {}).get('name', rows.get(event['item_id'], {}).get('skill', event['item_id']))
        recent.append(f'<tr><td>{escape(event["attempt_date_ist"][5:])}</td><td>{escape(title)}</td><td>{"Coding" if event.get("code_submission") else assessment_label(event)}</td><td><span class="rl-badge {result}">{escape(result.replace("_", " "))}</span></td></tr>')
    recent_panel = f'<section class="rl-panel rl-recent-panel"><div class="rl-section-head"><h2>Recent practice</h2><a class="rl-text-link" target="_self" href="{link("Revision Calendar")}">View history {icon("arrow")}</a></div><div class="rl-table-scroll"><table class="rl-table"><thead><tr><th>Date</th><th>Topic</th><th>Practice</th><th>Outcome</th></tr></thead><tbody>{"".join(recent)}</tbody></table></div>{"" if recent else "<div class=rl-empty>Your submitted attempts will appear here.</div>"}</section>'
    calendar = heatmap(activity, 'All Learning', settings['study_thresholds'], settings['attempt_thresholds'])
    calendar_panel = f'<section class="rl-panel rl-calendar-panel"><div class="rl-section-head"><div><h2>Small steps, over time</h2><p class="rl-section-description">Your recorded learning activity across the last year.</p></div><a class="rl-text-link" target="_self" href="{link("Revision Calendar")}">Explore calendar {icon("arrow")}</a></div>{calendar}<div class="rl-calendar-summary"><span><strong>{stats["active_days"]}</strong> active days</span><span><strong>{stats["hours"]:.1f} hrs</strong> confirmed study</span><span>Study time and assessments · IST</span></div></section>'
    return f'<div class="rl-dashboard"><div class="rl-page-heading"><div><span class="rl-eyebrow">YOUR LEARNING WORKSPACE</span><h2>Make room for what stays.</h2></div><span class="rl-dashboard-date">{today:%A, %d %B}</span></div>{hero}<div class="rl-overview">{metric_cells}</div><div class="rl-dashboard-grid"><div class="rl-primary-column">{task_panel}{recent_panel}</div><aside class="rl-secondary-column">{note_panel}{focus_panel}</aside></div>{calendar_panel}<div class="rl-dashboard-footnote">Practice is recorded as evidence. Activity alone does not imply mastery.</div></div>'


def assessment_label(event):
    if is_revision(event):
        return 'Revision'
    return {'initial_learning': 'Initial learning', 'diagnostic': 'Diagnostic',
            'application': 'Application', 'immediate_correction': 'Correction'}.get(event.get('review_kind'), 'Learning')


def PathLabel(path):
    return path.removeprefix('Notes/').removesuffix('.md')
