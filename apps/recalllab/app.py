"""RecallLab: local-first practice over the existing five-role learning records."""
import hashlib
import json
import os
from datetime import date, timedelta
from pathlib import Path
import sys
import tomllib

sys.path.insert(0, str(Path(__file__).resolve().parent))
import streamlit as st
from challenges.catalog import PYTHON, SQL
from components.calendar import heatmap
from services.bridge import end_session
from services.journal import Journal
from services.questions import Question, daily_queue, evaluate, question
from services.records import ROOT, Records, metrics, now, metric_events
from services.sql_runner import run_sql
from services.routing import PAGES, app_url, fingerprint, resolve
from services.notes import headings, section, render_links, relationships, blocks
from components.session_ui import daily_session
from components.assessment_ui import manual_review
from services.evaluation import sql_assessment

st.set_page_config(page_title='RecallLab', page_icon='◈', layout='wide')
st.markdown('<style>' + (Path(__file__).parent / 'components/theme.css').read_text(encoding='utf-8') + '</style>', unsafe_allow_html=True)
from components.dashboard import dashboard, brand, topbar

records = Records(Path(os.environ.get('RECALLLAB_ROOT', ROOT)))
journal = Journal(Path(os.environ['RECALLLAB_DATA']) / 'recalllab.sqlite3' if os.environ.get('RECALLLAB_DATA') else None)
today = now().date()
settings = {'session_minutes': 20, 'study_thresholds': [.25, .5, 1, 1.25], 'attempt_thresholds': [1, 3, 5, 8], 'coding_thresholds': [1, 2, 4, 6]}
config_path = Path(__file__).parent / 'config.toml'
if config_path.exists():
    settings.update(tomllib.loads(config_path.read_text(encoding='utf-8')))
settings.update(journal.get('settings', 'preferences', {}))
note_view_counter = 0


def navigate(destination, **values):
    if destination not in PAGES:
        return
    remembered = journal.get('settings', 'page:' + destination, {})
    params = dict(remembered, **{k:v for k,v in values.items() if v is not None}, view=destination)
    st.query_params.from_dict(params)
    st.session_state['_nav_query'] = fingerprint(params)
    journal.put('settings', 'last-page', params)


def sidebar_changed():
    navigate(st.session_state['route'])


def remember_calendar():
    values = {'metric':st.session_state.get('calendar-metric-'+page,'Revision Only' if page=='Revision Calendar' else 'All Learning'),
              'day':str(st.session_state.get('calendar-day-'+page,today))}
    journal.put('settings','page:'+page,values)
    navigate(page,**values)


def note_view(path, heading=None):
    global note_view_counter
    try:
        if not path.startswith('Notes/'):
            st.info('This concept has exercise evidence but no mapped explanation note.')
            st.caption(path)
            st.code(records.path(path).read_text(encoding='utf-8-sig'))
            return
        source = records.path(path, notes_only=True)
        text = source.read_text(encoding='utf-8-sig')
        options = ['Whole note'] + [h['key'] for h in headings(text)]
        desired = heading or journal.get('settings', 'note-section:' + path, 'Whole note')
        if desired not in options:
            import re
            desired = next((h['key'] for h in headings(text) if re.sub(r'[^a-z0-9]+','-',h['label'].lower()).strip('-') == desired), 'Whole note')
        note_view_counter += 1
        key = f'note-section-{note_view_counter}-' + hashlib.sha256((path + str(heading)).encode()).hexdigest()[:12]
        def section_changed():
            value = st.session_state[key]
            journal.put('settings','note-section:'+path,value)
            if page=='Notes Browser':
                prefs = dict(note=path)
                if value!='Whole note':
                    prefs['heading'] = value
                journal.put('settings','page:Notes Browser',prefs)
                navigate('Notes Browser',**prefs)
        selected = st.selectbox('Note section', options, index=options.index(desired), key=key,on_change=section_changed)
        journal.put('settings', 'note-section:' + path, selected)
        st.caption(path + (' · ' + selected if selected != 'Whole note' else ''))
        for kind, content in blocks(records,path,section(text,selected) if selected!='Whole note' else text):
            if kind=='image':
                st.image(content)
            elif kind=='caption':
                st.caption(content)
            else:
                st.markdown(render_links(records,path,content),unsafe_allow_html=False)
        topics, mistakes, exercises = relationships(records, path)
        with st.expander('Related concepts, mistakes and exercises'):
            for topic in topics:
                st.write(topic['id'], '—', topic['name'])
            for mistake in mistakes:
                st.write(mistake['mistake_id'], '—', mistake['observed_behaviour'])
            st.caption('Related exercises: ' + (', '.join(exercises) or 'None mapped'))
    except (OSError, ValueError) as error:
        st.warning(str(error))


def recommendations(events, namespace='recommendations'):
    recs = records.recommendations(events)
    if not recs:
        st.info('No mapped section recommendations are available for these attempts; check source evidence and mapping warnings.' if events else 'No assessed gaps yet. Submit a retrieval attempt to get specific section recommendations.')
    for i, rec in enumerate(recs):
        with st.container(border=True):
            st.markdown('**' + rec['heading'] + '**')
            st.caption(rec['path'])
            st.write(rec['gap'])
            st.caption('Attempt evidence: ' + rec['evidence'])
            with st.expander('Attempt that exposed this gap'):
                st.write(rec.get('question','Question evidence unavailable'))
                st.code(rec.get('answer','Answer evidence unavailable'))
            st.write(rec['action'])
            st.caption('Changed follow-up: '+rec.get('follow_up','Try a different input.'))
            if st.button('Open Note', key=f'{namespace}-open-{i}'):
                st.session_state['selected_note'] = rec
            if st.button('Retry', key=f'{namespace}-retry-{i}'):
                st.session_state['practice_item'] = rec['item_id']
                st.session_state['retry'] = st.session_state.get('retry', 0) + 1
                st.session_state['next_route'] = "Today's Session"
                st.rerun()
    if st.session_state.get('selected_note'):
        rec = st.session_state['selected_note']
        with st.expander('Recommended note', expanded=True):
            note_view(rec['path'], rec['heading'])


def annual_calendar(default_metric='All Learning'):
    modes = ['All Learning', 'Revision Only', 'Coding Practice']
    requested_metric = st.query_params.get('metric', default_metric)
    if requested_metric not in modes:
        requested_metric = default_metric
    metric = st.selectbox('Activity metric', ['All Learning', 'Revision Only', 'Coding Practice'],
                          index=modes.index(requested_metric),key='calendar-metric-'+page,on_change=remember_calendar)
    activity = records.activity(today)
    thresholds = settings['coding_thresholds'] if metric == 'Coding Practice' else settings['attempt_thresholds']
    st.markdown(heatmap(activity, metric, settings['study_thresholds'], thresholds, page=page), unsafe_allow_html=True)
    st.caption('Study uses confirmed closed intervals. Revision counts explicit revision-session submissions and delayed reviews only; initial learning, ordinary application and unlabelled same-day corrections are excluded. Revision time is not inferred from study time.')
    m = metrics(activity, metric)
    if metric == 'Revision Only' and not m['attempts']:
        st.info('Revision has not started yet. No revision attempts are recorded; study days do not count here.')
    columns = st.columns(5)
    for col, label, value in zip(columns, ['Active days', 'Current streak', 'Longest streak', 'Confirmed study hours' if metric == 'All Learning' else 'Duration', 'Revision attempts' if metric == 'Revision Only' else 'Coding submissions' if metric == 'Coding Practice' else 'Learning assessments'],
                                 [m['active_days'], m['current_streak'], m['longest_streak'], f'{m["hours"]:.1f}' if m['hours'] is not None else 'Not measured', m['attempts']]):
        col.metric(label, value)
    try:
        selected = date.fromisoformat(st.query_params.get('day', str(today)))
    except ValueError:
        selected = today
    selected = st.date_input('Day details (or click a calendar cell)', value=min(today, max(min(activity), selected)), min_value=min(activity), max_value=today,key='calendar-day-'+page,on_change=remember_calendar)
    d = activity[selected]
    selected_events = metric_events(d, metric)
    detail = f'{d["seconds"]/3600:.2f} confirmed study hours' if metric == 'All Learning' else f'{len(selected_events)} {"revision attempts" if metric == "Revision Only" else "coding submissions"}; duration not measured'
    with st.expander(f'{selected} · {detail}', expanded=bool(selected_events)):
        if metric == 'All Learning' and d['intervals']:
            st.dataframe(d['intervals'], hide_index=True)
        if selected_events:
            for event in selected_events:
                st.write(event['item_id'], '—', event.get('result', 'unknown'), '· score', event.get('score'))
                with st.expander(event.get('question', '')[:100]):
                    st.write(event.get('question')); st.code(event.get('answer', ''))
                    st.write(event.get('feedback', 'No feedback recorded'))
                    st.caption(event.get('evidence', 'Evidence unavailable'))
            recommendations(selected_events, 'day')
        else:
            st.caption('No revision attempts recorded for this day.' if metric == 'Revision Only' else 'No matching assessments recorded for this day.')
        attempt_ids = {e.get('attempt_id') for e in selected_events}
        observed = [dict(mistake_id=m['mistake_id'], gap=m['observed_behaviour']) for m in records.json('tracking/mistakes.json')['mistakes'] if any(o['observed_date_ist'] == str(selected) and (metric == 'All Learning' or o['attempt_id'] in attempt_ids) for o in m['observations'])]
        if observed:
            st.write('Observed mistakes'); st.dataframe(observed, hide_index=True)


def session_summary():
    sessions = journal.sessions()
    pending = [s for s in sessions if s['state'] != 'recorded' and journal.attempts(s['id'])]
    for s in pending:
        st.info(f'{len(journal.attempts(s["id"]))} attempts saved locally / pending canonical sync · {s["id"]}')
        if st.button('End session / save checkpoint' if s['state'] == 'open' else 'Retry interrupted checkpoint', key='end-' + s['id'], type='primary'):
            try:
                message = end_session(records, journal, s['id'])
                st.session_state['saved_checkpoint_message'] = message
                st.rerun()
            except (OSError, ValueError, KeyError) as error:
                st.error(f'Checkpoint remains recoverable and pending: {error}')
    return pending


def completed_report():
    report = journal.get('settings','last-report')
    if report:
        with st.expander('Last completed session · Notes to Review',expanded=True):
            st.write(report['summary'])
            st.caption(report['checkpoint_id']+' · recorded in canonical trackers; GitHub sync is separate')
            for i, rec in enumerate(report['recommendations']):
                st.markdown(f'**{rec["heading"]}** · `{rec["path"]}`')
                st.write(rec['gap']); st.caption('Evidence: '+rec['evidence'])
                with st.expander('Question and answer that exposed the gap'):
                    st.write(rec.get('question','See linked attempt evidence.'))
                    st.code(rec.get('answer','See linked attempt evidence.'))
                st.write(rec.get('follow_up',rec['action']))
                st.markdown(f'[Open section]({app_url("Notes Browser",note=rec["path"],heading=rec["heading"])})')


def practice():
    def mode_changed():
        extra = st.session_state['practice-mode']=='Extra concept practice'
        values = {'mode':'extra' if extra else 'daily'}
        if extra and st.session_state.get('practice_item'):
            values.update(item=st.session_state['practice_item'],question_day=st.session_state.get('practice_day',str(today)))
        journal.put('settings',"page:Today's Session",values)
        navigate("Today's Session",**values)
    mode = st.radio('Practice mode',['Daily session','Extra concept practice'],key='practice-mode',horizontal=True,on_change=mode_changed)
    if mode=='Daily session':
        daily_session(records,journal,today,settings,note_view,recommendations,session_summary)
    else:
        extra_practice()
    completed_report()


def extra_practice():
    minutes = st.slider('Revision budget (minutes)', 5, 45, int(settings['session_minutes']), step=5)
    queue = daily_queue(records, minutes, today)
    st.caption('A manageable selection with prerequisite checks. No tutor timer is started.')
    if queue:
        st.dataframe(queue, hide_index=True)
    items = [r['item_id'] for r in records.csv('revision-queue.csv')]
    default = st.session_state.get('practice_item') or (queue[0]['id'] if queue else items[0])
    def item_changed():
        value = st.session_state['practice-item-filter']
        st.session_state['practice_item'] = value
        st.session_state['practice_day'] = str(today)
        st.session_state['retry'] = 0
        values = dict(mode='extra',item=value,question_day=str(today))
        journal.put('settings',"page:Today's Session",values)
        navigate("Today's Session",**values)
    item = st.selectbox('Practice item', items, index=None if 'practice-item-filter' in st.session_state else items.index(default) if default in items else 0,key='practice-item-filter',on_change=item_changed)
    retry = st.session_state.get('retry', 0)
    practice_day = date.fromisoformat(st.session_state.get('practice_day', str(today)))
    q = question(records, item, practice_day, retry)
    session = journal.session()
    token = session + ':' + q.variant_id
    draft = journal.get('drafts', token, {})
    st.subheader(q.title)
    st.caption(q.mode + ' · ' + q.variant_id)
    st.markdown(q.prompt)
    answer_key = 'answer-' + token
    explanation_key = 'explanation-' + token
    if answer_key not in st.session_state:
        st.session_state[answer_key] = draft.get('answer', '')
        st.session_state[explanation_key] = draft.get('explanation', '')
    def persist_draft():
        old = journal.get('drafts', token, {})
        journal.put('drafts', token, dict(old, answer=st.session_state.get(answer_key, ''), explanation=st.session_state.get(explanation_key, ''), item_id=item, day=str(practice_day), retry=retry))
    answer = st.text_area('Your answer / code (JSON for output prediction)', key=answer_key, height=190, on_change=persist_draft)
    explanation = st.text_area('Reasoning and verification (assessed separately by your tutor)', key=explanation_key, on_change=persist_draft)
    hints = draft.get('hints', 0)
    notes_used = draft.get('notes_used', False)
    if st.button('Give me the next hint', disabled=hints >= len(q.hints)):
        hints += 1
        journal.put('drafts', token, dict(journal.get('drafts', token, {}), hints=hints))
        st.rerun()
    for hint in q.hints[:hints]:
        st.info(hint)
    if st.button('Consult source notes'):
        journal.put('drafts', token, dict(journal.get('drafts', token, {}), notes_used=True))
        st.rerun()
    if notes_used:
        st.caption('Notes consulted: this attempt is assisted.')
        sources = list(dict.fromkeys(s['path'] for s in q.sources))
        if sources:
            with st.expander('Source note', expanded=True):
                note_view(st.selectbox('Source', sources))
    help_choice = st.radio('Other help used?', ['Unknown / not stated', 'No help', 'Yes'], horizontal=True)
    help_used = {'Unknown / not stated': None, 'No help': False, 'Yes': True}[help_choice]
    if st.button('Submit Attempt', type='primary'):
        try:
            assessment = evaluate(q, answer, help_used, notes_used, hints)
            saved = journal.save(session, token, dict(item_id=item, question=q.prompt, answer=answer,
                            explanation=explanation, task_variant=q.variant_id, sources=q.sources,
                            dimension=q.dimension, hints_used=hints, notes_used=notes_used,
                            help_used=True if notes_used or hints else help_used, practice_context='revision', **assessment))
            st.success('Saved locally / pending sync: ' + saved['attempt_id'])
        except ValueError as error:
            st.error(str(error))
    saved = next((a for a in journal.effective_attempts(session) if a['task_variant'] == q.variant_id), None)
    if saved:
        st.write(saved['feedback'])
        with st.expander('Feedback / worked reference (after submission)'):
            st.write(q.solution)
        if st.button('Try a changed example'):
            st.session_state['retry'] = retry + 1
            st.rerun()
        recommendations(journal.effective_attempts(session), 'session')
    st.caption('Drafts persist after the text field loses focus (Tab or click outside). Settings lists recoverable drafts, including earlier question dates.')
    manual_review(journal,session,'extra-manual')
    session_summary()


def challenges():
    languages = ['Python (manual assessment)', 'SQL (disposable SQLite)']
    requested_language = languages[1] if st.query_params.get('language')=='SQL' or st.query_params.get('challenge','').startswith('sql-') else journal.get('settings','coding-language',languages[0])
    def language_changed():
        value = st.session_state['coding-language-filter']
        selected_bank = PYTHON if value.startswith('Python') else SQL
        st.session_state.pop('coding-challenge-filter',None)
        journal.put('settings','coding-language',value)
        values = dict(language='Python' if value.startswith('Python') else 'SQL',challenge=selected_bank[0][0])
        journal.put('settings','page:Coding Challenges',values)
        navigate('Coding Challenges',**values)
    language = st.radio('Language', languages, index=None if 'coding-language-filter' in st.session_state else languages.index(requested_language),horizontal=True,key='coding-language-filter',on_change=language_changed)
    journal.put('settings','coding-language',language)
    bank = PYTHON if language.startswith('Python') else SQL
    requested = st.query_params.get('challenge') or journal.get('settings','challenge:'+language,bank[0][0])
    def challenge_changed():
        selected = st.session_state['coding-challenge-filter']
        values = dict(language='Python' if language.startswith('Python') else 'SQL',challenge=selected[0])
        journal.put('settings','page:Coding Challenges',values)
        navigate('Coding Challenges',**values)
    challenge = st.selectbox('Challenge', bank, index=None if 'coding-challenge-filter' in st.session_state else next((i for i,c in enumerate(bank) if c[0]==requested),0),format_func=lambda x: x[2],key='coding-challenge-filter',on_change=challenge_changed)
    journal.put('settings','challenge:'+language,challenge[0])
    ident, item, title, prompt, *kind = challenge
    st.subheader(title); st.write(prompt)
    if kind:
        st.code('customers(customer_id INTEGER, name TEXT)\norders(order_id INTEGER, customer_id INTEGER, amount INTEGER)', language='sql')
        expected_sample = {'join':'(1,101), (1,102), (2,NULL), (3,103)', 'sum':'(1,Asha,7), (2,Asha,NULL), (3,Devi,0)', 'count':'(1,Asha,2), (2,Asha,0), (3,Devi,1)'}[kind[0]]
        st.caption('Sample: customers (1,Asha),(2,Asha),(3,Devi); orders (101,1,7),(102,1,NULL),(103,3,0). Expected rows: '+expected_sample+'. Tests use three fixtures. SQLite-compatible SQL only.')
    else:
        st.info('Run Tests disabled: no verified isolated Python runner is available. Submit source for manual tutor assessment. RecallLab never executes it.')
        with st.expander('Starter shape and verification checklist'):
            name = {'clean-records':'clean_orders','dictionary':'changed_copy','list-records':'active_ids','csv-read':'parse_rows','csv-write':'write_rows','files':'inspect_file','random':'generate_records'}[ident]
            st.code(f'def {name}(data):\n    # Implement the problem above using scratch inputs.\n    pass\n\n# Verify the sample, empty input and one changed edge case.\n# Preserve original inputs where required.',language='python')
    session = journal.session()
    retry = journal.get('settings','coding-retry:'+ident,0)
    token = f'{session}:code:{ident}:{retry}'
    key = 'code-' + token
    if key not in st.session_state:
        st.session_state[key] = journal.get('drafts', token, {}).get('answer', '')
    def save_code():
        journal.put('drafts', token, dict(journal.get('drafts', token, {}), answer=st.session_state[key]))
    code = st.text_area('Writable code editor', key=key, height=260, on_change=save_code)
    if st.button('Run Query' if kind else 'Run Tests', disabled=not kind):
        result = run_sql(code, kind[0])
        journal.put('drafts', token, dict(journal.get('drafts', token, {}), tests=result, tested_hash=hashlib.sha256(code.encode()).hexdigest()))
    draft = journal.get('drafts', token, {})
    result = draft.get('tests') if draft.get('tested_hash') == hashlib.sha256(code.encode()).hexdigest() else None
    if result:
        st.success('All controlled fixtures passed') if result['passed'] else st.warning('Tests did not pass')
        st.json(result)
    hints = draft.get('hints', 0)
    if st.button('Challenge hint'):
        journal.put('drafts', token, dict(draft, hints=hints + 1))
        st.rerun()
    if hints:
        st.info('Trace one input by hand; check empty input, NULL/missing values, and whether identity is preserved.')
    if st.button('Consult challenge notes'):
        journal.put('drafts', token, dict(draft, notes_used=True))
        st.rerun()
    notes_used = draft.get('notes_used', False)
    if notes_used:
        sources = question(records, item, today).sources
        if sources:
            note_view(sources[0]['path'], sources[0]['key'])
    declared = st.radio('Help declaration', ['Unknown', 'No help or notes beyond recorded hints', 'Other help used'])
    help_used = None if declared == 'Unknown' else declared == 'Other help used'
    if hints or notes_used:
        help_used = True
    if st.button('Submit Code Attempt', type='primary'):
        try:
            if result is None:
                assessment = dict(score=None,result='assisted' if help_used else 'unknown',feedback='Manual assessment pending. No passing tests or score claimed.',correct=None,evaluation='manual_pending',evaluation_status='not_evaluated',test_evidence=None)
            else:
                assessment = sql_assessment(result,help_used,notes_used,hints)
            saved = journal.save(session, token, dict(item_id=item, question=prompt, answer=code,
                       dimension='building', task_variant=f'{ident}-{retry}', assessment_kind='application',
                       help_used=help_used, hints_used=hints, notes_used=notes_used, code_submission=True,
                       sources=question(records,item,today).sources,correction_of=journal.get('settings',f'code-correction:{ident}:{retry}'),**assessment))
            st.success('Saved locally / pending sync: ' + saved['attempt_id'])
        except ValueError as error:
            st.error(str(error))
    if st.button('New code attempt'):
        previous = next((a for a in journal.attempts(session) if a.get('task_variant')==f'{ident}-{retry}'),None)
        if previous:
            journal.put('settings',f'code-correction:{ident}:{retry+1}',previous['attempt_id'])
        journal.put('settings','coding-retry:'+ident,retry+1)
        st.rerun()
    manual_review(journal,session,'coding-manual')
    st.subheader('Saved code history')
    history = [a for a in journal.effective_attempts() if a.get('code_submission') and a['item_id']==item]
    for a in reversed(history[-15:]):
        with st.expander(a['timestamp']+' · '+a.get('evaluation_status',a.get('result','unknown'))):
            st.code(a['answer'],language='sql' if kind else 'python')
            st.write(a['feedback'])
            if a.get('test_evidence'):
                st.json(a['test_evidence'])
    if not history:
        st.caption('No code submitted for this concept yet.')
    session_summary()


def analytics():
    events = records.events()
    scored = [e for e in events if e.get('score') is not None]
    independent = [e for e in scored if e.get('result') == 'independent']
    columns = st.columns(4)
    columns[0].metric('Assessed attempts', len(scored))
    columns[1].metric('Independent success (score ≥2)', f'{100*sum(e["score"]>=2 for e in independent)/len(scored):.0f}%' if scored else 'Unassessed')
    columns[2].metric('Delayed independent successes', sum(e.get('review_kind') == 'delayed' and e.get('score', 0) >= 2 for e in independent))
    columns[3].metric('Unscored / unknown assessments', len(events) - len(scored))
    st.caption('Activity and accuracy are separate. Output tests do not assess explanation. Assisted success is not independent retention.')
    objective = [e for e in events if type(e.get('correct')) is bool]
    st.metric('Verified output accuracy (help included)', f'{100*sum(e["correct"] for e in objective)/len(objective):.0f}%' if objective else 'No explicit output assessments')
    code_tests = [e for e in events if e.get('code_submission') and e.get('test_evidence')]
    st.metric('Coding test pass rate',f'{100*sum(e["test_evidence"]["passed"] for e in code_tests)/len(code_tests):.0f}%' if code_tests else 'Not evaluated')
    st.caption('Human assessments are labelled human_review in evidence; executable test outcomes are counted separately above.')
    state, _ = records.coverage(today)
    st.write(state['coverage'])
    st.dataframe([{k: t.get(k) for k in ('id', 'name', 'state', 'delayed_practised', 'initial_assessment_date_ist')} for t in state['topics']], hide_index=True)
    st.subheader('Dimension-specific evidence')
    st.dataframe(records.json('tracking/skill-state.json')['observations'], hide_index=True)
    st.subheader('Weekly confirmed activity')
    activity = records.activity(today)
    weeks = {}
    for d, v in activity.items():
        key = str(d - timedelta(days=d.weekday()))
        weeks[key] = weeks.get(key, 0) + v['seconds'] / 3600
    st.bar_chart({'Confirmed hours': weeks})


def settings_page():
    st.caption('Offline deterministic questions are always available. Optional AI explanations are off unless you explicitly enable a local provider below.')
    minutes = st.select_slider('Default session minutes', options=list(range(5, 61, 5)), value=int(settings['session_minutes']))
    study = st.text_input('Study intensity thresholds (fractions of daily target)', value=','.join(str(x) for x in settings['study_thresholds']))
    counts = st.text_input('Revision intensity thresholds (attempt counts)', value=','.join(str(x) for x in settings['attempt_thresholds']))
    coding = st.text_input('Coding intensity thresholds (attempt counts)', value=','.join(str(x) for x in settings['coding_thresholds']))
    if st.button('Save preferences'):
        try:
            a = [float(x) for x in study.split(',')]; b = [int(x) for x in counts.split(',')]; c = [int(x) for x in coding.split(',')]
            if len(a) != 4 or len(b) != 4 or len(c) != 4 or a != sorted(set(a)) or b != sorted(set(b)) or c != sorted(set(c)) or min(a) <= 0 or min(b) < 1 or min(c) < 1 or a[-1] <= 1:
                raise ValueError('Use four increasing positive thresholds; highest study threshold must exceed the target.')
            journal.put('settings', 'preferences', dict(session_minutes=minutes, study_thresholds=a, attempt_thresholds=b, coding_thresholds=c))
            st.success('Local preferences saved')
        except ValueError as error:
            st.error(str(error))
    st.download_button('Export local recovery journal (JSON)', data=journal.export(), file_name='recalllab-recovery.json', mime='application/json')
    if st.button('Create consistent local SQLite backup'):
        st.success(str(journal.backup()))
    recovery = st.file_uploader('Import your trusted RecallLab recovery export',type=['json'])
    if st.button('Import pending journal',disabled=recovery is None):
        try:
            journal.backup()
            st.success(journal.restore_export(recovery.getvalue().decode('utf-8-sig')))
        except (ValueError,OSError) as error:
            st.error('Import did not replace existing records: '+str(error))
    with st.expander('Optional local Ollama · disabled by default'):
        ai = journal.get('settings','local-ai',{})
        with st.form('local-ai-settings'):
            endpoint = st.text_input('Local Ollama base URL',value=ai.get('endpoint','http://127.0.0.1:11434'))
            model = st.text_input('Installed local model name',value=ai.get('model',''))
            enabled = st.checkbox('Opt in: allow submitted answers and their source section to be sent to my local Ollama process for explanatory feedback',value=ai.get('enabled',False))
            if st.form_submit_button('Save local AI preference'):
                from urllib.parse import urlsplit
                parsed = urlsplit(endpoint)
                if enabled and (parsed.scheme!='http' or parsed.hostname not in ('127.0.0.1','localhost','::1') or not model.strip() or parsed.username or parsed.password):
                    st.error('Use an installed model and a loopback HTTP endpoint. External providers are not configured.')
                else:
                    journal.put('settings','local-ai',dict(enabled=enabled,endpoint=endpoint,model=model))
                    st.success('Local preference saved. No request was sent; explanations require a separate button after submitting an answer.')
    st.warning('Local drafts and pending submissions do not sync between computers. End the session, then intentionally commit/push evidence and canonical records; pull on the other computer. An export/backup contains private answers: keep it local.')
    session_summary()
    st.subheader('Prior local sessions')
    for s in journal.sessions():
        with st.expander(s['created'] + ' · ' + s['state']):
            st.json(journal.attempts(s['id']))
    st.subheader('Recoverable question drafts')
    for key, draft in journal.drafts():
        if draft.get('item_id') and draft.get('answer'):
            with st.expander(draft['item_id'] + ' · ' + draft.get('day', '')):
                st.code(draft['answer'])
                if st.button('Resume this draft', key='resume-' + key):
                    st.session_state['practice_item'] = draft['item_id']
                    st.session_state['practice_day'] = draft['day']
                    st.session_state['retry'] = draft.get('retry', 0)
                    st.session_state['next_route'] = "Today's Session"
                    st.rerun()


st.sidebar.markdown(brand(), unsafe_allow_html=True)
query = st.query_params.to_dict()
if 'next_route' in st.session_state:
    destination = st.session_state.pop('next_route')
    st.session_state['route'] = destination
    if destination=="Today's Session" and st.session_state.get('practice_item'):
        st.session_state['practice-mode'] = 'Extra concept practice'
    navigate(destination, item=st.session_state.get('practice_item'))
elif fingerprint(query) != st.session_state.get('_nav_query'):
    if query:
        destination = resolve(query)
        st.session_state['route'] = destination
        journal.put('settings', 'last-page', dict(query, view=destination))
        if query.get('item') in {r['item_id'] for r in records.csv('revision-queue.csv')}:
            st.session_state['practice_item'] = query['item']
            st.session_state['practice-item-filter'] = query['item']
            st.session_state['practice_day'] = query.get('question_day',str(today))
            st.session_state['practice-mode'] = 'Extra concept practice'
        elif destination == "Today's Session":
            st.session_state['practice-mode'] = 'Extra concept practice' if query.get('mode')=='extra' else 'Daily session'
        if destination=='Coding Challenges' and (query.get('challenge') or query.get('language')):
            sql = query.get('language')=='SQL' or query.get('challenge','').startswith('sql-')
            st.session_state['coding-language-filter'] = 'SQL (disposable SQLite)' if sql else 'Python (manual assessment)'
            target = next((c for c in (SQL if sql else PYTHON) if c[0]==query.get('challenge')),None)
            if target:
                st.session_state['coding-challenge-filter'] = target
    else:
        remembered = journal.get('settings', 'last-page', {'view':'Dashboard'})
        st.session_state['route'] = resolve(remembered)
        navigate(st.session_state['route'])
    st.session_state['_nav_query'] = fingerprint(st.query_params.to_dict())
nav_icons = ['⌂', '☷', '▣', '⌘', '▤', '◎', '▥', '▦', '⌕', '⚙']
page = st.sidebar.radio('Workspace', PAGES, key='route', on_change=sidebar_changed, format_func=lambda p: nav_icons[PAGES.index(p)] + '    ' + p)
side_metric = 'Revision Only' if page == 'Revision Calendar' else 'All Learning'
side_stats = metrics(records.activity(today), side_metric)
side_label = 'Revision Streak' if side_metric == 'Revision Only' else 'Learning Streak'
st.sidebar.markdown(f'<div class="rl-sidecard">🔥 {side_label}<strong>{side_stats["current_streak"]} days</strong><small>Best: {side_stats["longest_streak"]} days · {"revision attempts" if side_metric == "Revision Only" else "confirmed activity"}</small></div>', unsafe_allow_html=True)
st.sidebar.markdown('---')
st.sidebar.caption('Learning continuity: START-HERE.md\nActive project: RRDAP / RDS-001')
pending_count = sum(len(journal.attempts(s['id'])) for s in journal.sessions() if s['state'] != 'recorded')
if pending_count:
    st.sidebar.warning(f'{pending_count} locally saved attempts pending canonical sync')
st.markdown(topbar(today), unsafe_allow_html=True)
if page != 'Dashboard':
    st.title(page)
if 'saved_checkpoint_message' in st.session_state:
    st.success(st.session_state.pop('saved_checkpoint_message'))
try:
    state, live = records.coverage(today)
    from services.records import load_coach
    try:
        load_coach(records.root).note_revision.check(records.root, records.json('tracking/topic-map.json'))
    except ValueError as warning:
        with st.sidebar.expander('Records notice · note inventory', expanded=False):
            st.caption('Scores and due dates are preserved. ' + str(warning))
    if state['gaps']:
        st.warning('Notes coverage needs mapping: ' + '; '.join(state['gaps'][:3]))
    changed = [t['id'] for t in live['topics'] if t.get('needs_reassessment')]
    if changed:
        st.warning('Changed source sections need inspection (history preserved): ' + ', '.join(changed))
    if page == 'Dashboard':
        st.markdown(dashboard(records, journal, today, settings), unsafe_allow_html=True)
        session_summary()
        if st.query_params.get('day'):
            with st.expander('Selected calendar day ? recorded evidence', expanded=True):
                annual_calendar()
    elif page == 'Revision Calendar':
        annual_calendar('Revision Only')
        st.subheader('Scheduled follow-ups')
        st.caption('Planned dates are separate from completed attempts and unassessed diagnostic slots.')
        st.dataframe([dict(item=r['item_id'], due=r['next_review_date_ist'], result=r['last_result']) for r in records.csv('revision-queue.csv') if r['next_review_date_ist']], hide_index=True)
        st.subheader('Initial diagnostic planning slots')
        st.dataframe([dict(item=t['id'], proposed=t.get('initial_assessment_date_ist'), state=t['state']) for t in state['topics'] if t['state'] == 'Unassessed'], hide_index=True)
    elif page == "Today's Session":
        practice()
    elif page == 'Coding Challenges':
        challenges()
    elif page == 'Question Bank':
        text = st.text_input('Filter by topic, mode, source or evidence ID',value=journal.get('settings','bank-filter',''),key='bank-filter',on_change=lambda:journal.put('settings','bank-filter',st.session_state['bank-filter']))
        for row in records.csv('revision-queue.csv'):
            q = question(records, row['item_id'], today)
            linked = [e for e in records.events() if e['item_id'] == q.item_id]
            blob = json.dumps({'question': q.dict(), 'evidence': linked})
            if text.lower() not in blob.lower():
                continue
            with st.expander(q.title + ' · ' + q.item_id + ' · ' + q.mode):
                st.markdown(q.prompt)
                st.caption('Sources: ' + '; '.join(s['path'] + ' / ' + s['key'] for s in q.sources))
                if st.button('Practise this', key='bank-' + q.item_id):
                    st.session_state['practice_item'] = q.item_id
                    st.session_state['next_route'] = "Today's Session"
                    st.rerun()
    elif page == 'Notes Browser':
        paths = records.notes()
        if st.query_params.get('recommended'):
            recommendations(journal.attempts()[-10:] or records.events()[-10:], 'notes-browser')
        if paths:
            requested_note = st.query_params.get('note') or journal.get('settings','page:Notes Browser',{}).get('note')
            def note_changed():
                prefs = {'note':st.session_state['original-note']}
                journal.put('settings','page:Notes Browser',prefs)
                navigate('Notes Browser',**prefs)
            chosen_note = st.selectbox('Original note', paths, index=paths.index(requested_note) if requested_note in paths else 0,key='original-note',on_change=note_changed)
            note_view(chosen_note, st.query_params.get('heading') if chosen_note == requested_note else None)
        else:
            st.info('No Markdown notes available in this checkout.')
    elif page == 'Search Notes':
        query = st.text_input('Search original notes',value=journal.get('settings','search',''),key='search',on_change=lambda:journal.put('settings','search',st.session_state['search']))
        if query.strip():
            matches = [(p, records.path(p, True).read_text(encoding='utf-8-sig')) for p in records.notes()]
            found = [(p, t) for p, t in matches if query.casefold() in t.casefold() or query.casefold() in p.casefold()]
            st.caption(f'{len(found)} matching notes')
            for path, content in found:
                with st.expander(path):
                    st.markdown(content, unsafe_allow_html=False)
    elif page == 'Mistakes & Weak Topics':
        for m in records.json('tracking/mistakes.json')['mistakes']:
            with st.expander(m['mistake_id'] + ' · ' + m['status'] + ' · ' + m['observed_behaviour']):
                st.write(m['expected_behaviour']); st.write(m['follow_up_task'])
                st.caption('Cause confidence: ' + m['cause']['confidence'])
                st.dataframe(m['observations'], hide_index=True)
        st.subheader('Current concept states')
        st.dataframe([{k: t.get(k) for k in ('id', 'state', 'prerequisites')} for t in state['topics']], hide_index=True)
    elif page == 'Progress & Analytics':
        analytics()
    elif page == 'Settings':
        settings_page()
except (OSError, ValueError, KeyError) as error:
    st.error(f'Records need attention: {error}. Your existing learning records have not been replaced. See README recovery instructions.')
