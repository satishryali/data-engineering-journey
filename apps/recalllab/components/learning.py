"""Read-only schedule, roadmap, project and interview views over repository authorities."""
import importlib.util
import re
import streamlit as st
from services.records import study_plan


def document(records, path):
    text = records.path(path).read_text(encoding='utf-8')
    # These read-only project/plan pages are not a repository file server.
    # Keep official web references clickable and render local document labels plainly.
    text = re.sub(r'\[([^]]+)\]\((?!https?://)[^)]*\)', r'\1', text)
    st.markdown(text)


def next_task(records):
    text = records.path('progress/current.md').read_text(encoding='utf-8-sig')
    return text.split('## Exact next task', 1)[1].split('\n## ', 1)[0].strip()


def bank(records):
    spec = importlib.util.spec_from_file_location('recalllab_interview', records.root / 'tracking/interview.py')
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module, module.load(records.root)


def overview(records, today):
    targets = study_plan.summary(records.root, str(today))
    st.subheader("Today's study schedule")
    cols = st.columns(4)
    for col, label, value in zip(cols, ['Daily target', 'Confirmed today', 'Week target', 'Confirmed this week'],
                                  [targets['daily_target_hours'], targets['confirmed_today_hours'],
                                   targets['weekly_target_hours'], targets['confirmed_week_hours']]):
        col.metric(label, f'{value:.2f} h')
    st.caption(f"Week {targets['week_start']}–{targets['week_end']} IST. Remaining today {targets['remaining_today_hours']:.2f} h; closed-day shortfall this week {targets['closed_day_shortfall_hours']:.2f} h. Running/uncertain time excluded.")
    rows = study_plan.roadmap_rows(records.root)
    current = next((r for r in rows if r['start_date_ist'] <= str(today) <= r['end_date_ist']), None)
    st.write('Planned primary focus: ' + (current['main_focus'] if current else 'Checkpoint priorities / verification'))
    st.write('Actual pending task: ' + next_task(records))
    st.write('Independent practice: submit the next bounded implementation and actual checks against its acceptance criteria.')
    st.caption('Carry forward unfinished work until accepted. The checkpoint retains earlier deferred work. Selecting a view starts no study timer.')
    if str(today) >= study_plan.config(records.root)['preparation_start']:
        field = 'weekend_hours' if today.weekday() >= 5 else 'weekday_hours'
        st.dataframe([{'Activity': r['activity'], 'Hours': r[field]} for r in study_plan.activity_rows(records.root)], hide_index=True)
    _, questions = bank(records)
    assessed = {(e.get('assessment') or {}).get('question_id') for e in records.events()}
    st.write(f'Interview practice: {len(assessed & {q["id"] for q in questions})} question IDs with saved assessment metadata. Readiness requires reviewed evidence.')
    st.caption('Suggested foundation interview: INT-SQL-001 in Interview Practice. Bounded due revision remains in the existing dashboard suggestions.')


def roadmap(records):
    st.write('Preparation: 22 October 2026–22 January 2027. Thirteen Thursday–Wednesday weeks, then 21–22 January verification buffer.')
    st.caption('All milestones are planned. Actual project acceptance and assessed dimensions establish progress; elapsed dates and hours do not complete a row.')
    st.dataframe(study_plan.roadmap_rows(records.root), hide_index=True)
    st.write('Actual pending work: ' + next_task(records))
    with st.expander('Technology requirements, prerequisites and daily allocations'):
        document(records, 'plan/learning-and-revision-plan.md')


def project(records):
    document(records, 'projects/rrdap/checkpoint.md')
    with st.expander('RDS-001 acceptance criteria and assignment'):
        document(records, 'projects/rrdap/tasks/RDS-001.md')
    with st.expander('Project phases and scope'):
        document(records, 'projects/rrdap/roadmap.md')
    st.caption('Tests, decisions and incident reports need actual evidence. Engineering templates are available; no completed outcome is implied.')


def interview(records):
    module, questions = bank(records)
    chosen = st.selectbox('Interview question', [q['id'] for q in questions],
                          format_func=lambda ident: next(f'{q["id"]} · {q["category"]} · {q["difficulty"]}' for q in questions if q['id']==ident))
    prompt = module.present(questions, chosen)
    st.caption(f'{prompt["difficulty"]} · suggested {prompt["minutes"]} minutes; no timer started')
    st.write(prompt['scenario'])
    st.write(prompt['task'])
    st.code(prompt['sample_input'])
    st.write('Expected result: ' + prompt['expected_output'])
    st.info('Attempt independently first. Share code, output, reasoning and help used with the tutor for review and checkpointing.')
    st.caption('This view presents prompts. Existing Coding Challenges provides its supported editor and SQL fixture tests. PostgreSQL/PySpark execution and automatic interview grading are unavailable.')


def interview_progress(records, today):
    _, questions = bank(records)
    events, rows = records.events(), []
    for q in questions:
        actual = [e for e in events if (e.get('assessment') or {}).get('question_id') == q['id']]
        latest = actual[-1] if actual else {}
        rows.append({'Category': q['category'], 'Question': q['id'],
                     'Latest result': latest.get('result', 'unassessed'),
                     'Help used': str(latest.get('help_used', 'unknown')),
                     'Evidence': latest.get('evidence', '')})
    st.subheader('Interview evidence by category')
    st.dataframe(rows, hide_index=True)
    targets = study_plan.summary(records.root, str(today))
    st.subheader('Confirmed hours by source topic')
    st.dataframe([{'Source topic': topic, 'Hours': hours} for topic, hours in targets['confirmed_hours_by_source_topic'].items()], hide_index=True)
    st.caption('Exact source labels retain mixed/setup attribution. Hours do not establish technology proficiency.')
