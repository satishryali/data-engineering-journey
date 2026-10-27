"""Problem-first practice inside RecallLab's existing journal and checkpoint flow."""
import json
import uuid

import streamlit as st

from services.curriculum import get_problem, list_technologies, cached_curriculum, published_problems, prerequisite_coverage, prerequisites_met, missing_prerequisites, pathway_status
from services.problems import Problems


def _select_tool(journal, tool_id):
    journal.put('settings', 'tools-selected', tool_id)
    st.session_state['tools-technology'] = tool_id


def _data(value):
    if isinstance(value, str):
        st.code(value)
    else:
        st.code(json.dumps(value, ensure_ascii=False, indent=2), language='json')


def _brief(problem):
    st.subheader(problem['title'])
    st.caption(f"{problem['id']} · Level {problem['level']} · About {problem['estimated_minutes']} minutes")
    st.write(problem['scenario'])
    st.markdown('**Your task**')
    st.write(problem['task'])
    st.markdown('**Input / environment**')
    _data(problem['inputs'])
    st.markdown('**Expected output**')
    _data(problem['expected_output'])
    for label, key in [('Constraints', 'constraints'), ('Acceptance criteria', 'acceptance_criteria')]:
        st.markdown('**' + label + '**')
        for line in problem[key]:
            st.markdown('- ' + line)
    st.caption('Real engineering responsibility: ' + problem['engineering_relevance'])


def _review(flow, journal, tool_id):
    pending = [a for a in flow.attempts() if a.get('tool_id') == tool_id and a.get('evaluation') == 'manual_pending']
    # A checkpoint freezes prior submissions. Pending work from frozen sessions is
    # still visible as evidence, but requires a fresh reviewed submission.
    open_sessions = {s['id'] for s in journal.sessions() if s['state'] == 'open'}
    pending = [a for a in pending if a.get('app_session_id') in open_sessions]
    if not pending:
        return
    with st.expander('Review submitted implementation', expanded=True):
        selected = st.selectbox('Submission to review', pending,
            format_func=lambda a: a['item_id'] + ' · ' + a['attempt_id'][-8:], key='tools-review-attempt')
        st.code(selected['answer'])
        st.write('Approach: ' + selected.get('how_solved', ''))
        st.write('Help: ' + ', '.join(selected.get('assistance_sources', ['unknown'])))
        st.markdown('**Submitted results**')
        st.code(selected.get('submitted_results', ''))
        if selected.get('explanation'):
            st.write(selected['explanation'])
        for criterion in get_problem(selected['problem_id'])['acceptance_criteria']:
            st.markdown('- ' + criterion)
        st.caption('Verification requires the actual implementation, output and acceptance checks. A saved submission alone does not complete a problem.')
        with st.form('tools-review'):
            reviewer = st.text_input('Reviewer name / role', key='tools-reviewer')
            verification = st.text_area('Observed output and edge-case checks', key='tools-verification')
            feedback = st.text_area('Feedback: correctness, mistakes, pipeline relevance and limitations', key='tools-feedback')
            score = st.selectbox('Review outcome', [None, 0, 1, 2, 3],
                format_func=lambda v: {None:'Choose after reviewing', 0:'Major gap', 1:'Partial implementation', 2:'Incomplete verification', 3:'All acceptance criteria verified'}[v])
            attested = st.checkbox('I checked the implementation, actual results, edge cases and all acceptance criteria.', key='tools-acceptance')
            if st.form_submit_button('Save problem review'):
                try:
                    flow.review(selected['attempt_id'], reviewer=reviewer, verification=verification,
                        feedback=feedback, score=score, acceptance_checked=attested)
                    st.session_state['tools-message'] = 'Review saved. Verified progress and the next challenge are ready below.'
                    st.rerun()
                except ValueError as error:
                    st.error(str(error))


def tools_page(records, journal):
    curriculum = cached_curriculum()
    flow = Problems(journal, catalog=curriculum, records=records)
    technologies = list_technologies(curriculum)
    names = {t['id']: t['name'] for t in technologies}
    tool_ids = list(names)
    remembered = journal.get('settings', 'tools-selected', tool_ids[0])
    if remembered not in tool_ids:
        remembered = tool_ids[0]
    tool_id = st.selectbox('Technology', tool_ids, index=tool_ids.index(remembered),
        format_func=lambda ident: names[ident], key='tools-technology')
    journal.put('settings', 'tools-selected', tool_id)
    progress = flow.progress(tool_id)
    st.write(f"{names[tool_id]} — {progress['completed']} / {progress['total']} problems completed")
    st.write(f"Independent mastery — {progress['independent']} / {progress['total']}")
    st.caption(f"Current level: {progress.get('current_level', 0)} · Next problem: {progress.get('next_problem_number') or 'none eligible'}")
    completed_ids, independent_ids = flow._ids()
    st.write(f"Overall — {len(completed_ids)} / {len(curriculum['problems'])} verified; {len(independent_ids)} independently mastered")
    job_ready = st.checkbox('Use the curated January 20 Job-Ready pathway',
        value=journal.get('settings','tools-job-path',False), key='tools-job-path')
    journal.put('settings','tools-job-path',job_ready)
    if job_ready:
        path = pathway_status(completed_ids, independent_ids, curriculum)
        st.caption(f"Job-Ready pathway: {path['completed']} / {path['total']} verified. The full bank is not required for assessment eligibility.")
        st.dataframe(path['assessments'],hide_index=True)
    version = str(curriculum.get('version', '1'))
    st.caption('Published curriculum ' + version + ' · Only verified published problems count. Assistance never erases progress.')
    seen = journal.get('settings', 'tools-curriculum-version')
    snapshot = dict(version=version, totals={t['id']:t['published_total'] for t in technologies})
    if seen is None:
        journal.put('settings', 'tools-curriculum-version', snapshot)
    elif seen['version'] != version:
        st.info(f"Curriculum expanded: {seen['version']} → {version}. {names[tool_id]} published total: "
            f"{seen['totals'].get(tool_id, 0)} → {progress['total']}. Historical completions and stable problem IDs are preserved.")
        if st.button('Acknowledge curriculum update', key='tools-version-ack'):
            journal.put('settings', 'tools-curriculum-version', snapshot)
            st.rerun()
    if progress.get('milestone'):
        st.success(f"Milestone reached: {progress['completed']} verified problems. Keep building on that work.")
    if progress.get('next_problem_id'):
        st.caption('Next challenge — ' + str(progress['next_problem_id']))
    if progress.get('independent_followups'):
        for followup in progress['independent_followups']:
            st.info(f"Independent practice: {followup['problem_id']} · Due {followup['due_date']} · {followup['task']}")
            if st.button('Open changed-input independent practice', key='tools-followup-' + followup['problem_id']):
                try:
                    flow.independent_problem(followup['problem_id'])
                    journal.put('drafts', 'tools-active:' + tool_id,
                        dict(problem_id=followup['problem_id'], submission_open=False, independent_followup=True))
                    st.rerun()
                except ValueError as error:
                    st.info(str(error))
    if st.session_state.get('tools-message'):
        st.success(st.session_state.pop('tools-message'))

    state_key = 'tools-active:' + tool_id
    state = journal.get('drafts', state_key, {})
    diagnostics = flow.acceleration_options(tool_id)
    if diagnostics:
        with st.expander('Verify existing skills for faster progression'):
            st.caption('Choose one bounded practical assessment. Only verified independent work can cover its stated prerequisites; skipped tasks receive no completion credit.')
            diagnostic = st.selectbox('Practical assessment', diagnostics,
                format_func=lambda p: p['id'] + ' · ' + p['title'], key='tools-diagnostic-select')
            if st.button('Open practical assessment', key='tools-diagnostic-open'):
                candidate = flow.diagnostic_problem(diagnostic['id'])
                state = dict(problem_id=candidate['id'], submission_open=False, diagnostic=True)
                journal.put('drafts', state_key, state)
    with st.form('tools-command-form', clear_on_submit=True):
        command = st.text_input('Command', placeholder='/problem /hint /stuck /solved /next /review /progress /why', key='tools-command')
        sent = st.form_submit_button('Send command')
    if sent:
        if command.strip().lower() in ('/problem', '/next'):
            candidate = flow.next_problem(tool_id, job_ready=job_ready)
            if candidate:
                state = dict(problem_id=candidate['id'], submission_open=False)
                journal.put('drafts', state_key, state)
            else:
                completed = {a['problem_id'] for a in flow.attempts() if flow.verified(a)}
                independent = {a['problem_id'] for a in flow.attempts() if flow.verified(a)
                    and a.get('result') == 'independent' and a.get('help_used') is False}
                covered = prerequisite_coverage(independent, curriculum)
                remaining = [p for p in published_problems(tool_id, curriculum) if p['id'] not in completed | covered
                    and (not job_ready or p['id'] in curriculum.get('job_ready_pathway',{}).get('problem_ids',[]))]
                if remaining:
                    missing = sorted({ident for p in remaining
                        for group in missing_prerequisites(p,completed,independent,curriculum) for ident in group})
                    if missing:
                        st.info('This published path is waiting for prerequisite evidence (including independence where required): ' + ', '.join(missing)
                            + '. Choose the prerequisite technology below and use /problem for its next achievable task.')
                        bridge_tools = list(dict.fromkeys(get_problem(ident)['tool_id'] for ident in missing if get_problem(ident)))
                        for bridge_tool in bridge_tools:
                            st.button('Practise prerequisite: ' + names[bridge_tool], key='tools-bridge-' + bridge_tool,
                                on_click=_select_tool, args=(journal, bridge_tool))
                    else:
                        st.info('Your highest published stage is complete. Optional earlier-level breadth remains in Browse published challenges; it receives credit only if actually verified.')
                else:
                    st.info('The current published path is complete through verified work and any independent diagnostic coverage. '
                        'Counters include actual verified problem completions only. Future levels will be published in a versioned expansion.')
        elif command.strip().lower() == '/solved':
            if state.get('problem_id'):
                state['submission_open'] = True
                journal.put('drafts', state_key, state)
            else:
                st.info('Use /problem to open your next achievable task first.')
        elif command.strip().lower() in ('/hint', '/stuck'):
            if state.get('problem_id'):
                state['help_message'] = flow.hint(state['problem_id'], bool(state.get('independent_followup')))
                if command.strip().lower() == '/stuck':
                    state['help_message'] += '\nShare the smallest failing input, actual output or error, and what you expected. Preserve your original attempt.'
                journal.put('drafts',state_key,state)
            else:
                st.info('Open a problem before requesting a hint.')
        elif command.strip().lower() == '/why':
            problem = get_problem(state.get('problem_id'), curriculum)
            st.info(problem['engineering_relevance'] if problem else 'Open a problem to see its business purpose and engineering responsibility.')
        elif command.strip().lower() == '/progress':
            st.info(f"{names[tool_id]}: {progress['completed']} / {progress['total']} verified; {progress['independent']} independent. Current level {progress.get('current_level',0)}. Saved attempts determine these counts.")
        elif command.strip().lower() == '/review':
            state['review_open'] = True
            journal.put('drafts',state_key,state)
        else:
            st.info('Supported commands: /problem, /hint, /stuck, /solved, /next, /review, /progress, /why.')
    if not state.get('problem_id'):
        st.info('Type /problem to begin. Choosing a tool does not start a study timer.')
    else:
        problem = (flow.independent_problem(state['problem_id']) if state.get('independent_followup') else
            flow.diagnostic_problem(state['problem_id']) if state.get('diagnostic') else get_problem(state['problem_id']))
        _brief(problem)
        if state.get('help_message'):
            st.info(state['help_message'])
        if state.get('submission_open'):
            _submission(flow, journal, state_key, state)
    _review(flow, journal, tool_id)
    submitted = [a for a in flow.attempts() if a.get('tool_id') == tool_id]
    if state.get('review_open'):
        if submitted:
            st.dataframe([dict(problem=a['problem_id'],date=a['attempt_date_ist'],status=a.get('evaluation_status'),
                feedback=a.get('feedback'),help=a.get('assistance_sources')) for a in submitted],hide_index=True)
        else:
            st.info('No submitted implementation to review yet. Use /solved after an attempt; reviews never infer completion from a declaration.')
    if submitted:
        last = submitted[-1]
        st.markdown('**Latest review / verification**')
        st.write(flow.feedback(last))
        tests = last.get('test_evidence')
        if tests:
            with st.expander('Executed SQL fixture results', expanded=last.get('correct') is False):
                for number, fixture in enumerate(tests.get('fixtures', []), 1):
                    st.write(f"Fixture {number}: {'passed' if fixture['passed'] else 'needs correction'}")
                    st.write('Expected rows')
                    _data(fixture.get('expected', []))
                    st.write('Actual rows')
                    _data(fixture.get('actual', []))
                    if fixture.get('expected_columns') != fixture.get('actual_columns'):
                        st.write('Expected columns:', fixture.get('expected_columns'))
                        st.write('Actual columns:', fixture.get('actual_columns'))
                if tests.get('error'):
                    st.error(tests['error'])
        if last.get('correct') is True:
            st.caption('Use /problem for the next prerequisite-appropriate challenge. Assisted work remains completed; independent evidence is counted separately.')
    with st.expander('Progress by technology'):
        rows = [dict(technology=t['name'], **{k:v for k,v in flow.progress(t['id']).items()
            if k in ('completed', 'independent', 'total')}) for t in technologies]
        st.dataframe(rows, hide_index=True)
        if st.checkbox('Show overall Job-Ready track', key='tools-overall'):
            job_ids = {t['name'] for t in technologies if t.get('job_ready_track', t['priority'] == 'job_ready')}
            job_rows = [r for r in rows if r['technology'] in job_ids]
            st.write('Job-Ready track — ' + str(sum(r['completed'] for r in job_rows)) + ' / '
                + str(sum(r['total'] for r in job_rows)) + ' published problems verified')
    with st.expander('Browse published challenges'):
        levels = sorted({p['level'] for p in curriculum['problems'] if p['tool_id'] == tool_id})
        level = st.selectbox('Challenge level',levels,key='tools-browse-level')
        choices = [p for p in published_problems(tool_id,curriculum) if p['level'] == level]
        chosen = st.selectbox('Published challenge',choices,format_func=lambda p:p['id']+' · '+p['title'],key='tools-browse-problem')
        eligible = prerequisites_met(chosen,completed_ids,independent_ids,curriculum)
        st.caption('Prerequisites: '+(', '.join(chosen.get('prerequisites',[])) or 'none'))
        if st.button('Open published challenge',disabled=not eligible,key='tools-browse-open'):
            journal.put('drafts',state_key,dict(problem_id=chosen['id'],submission_open=False))
            st.rerun()


def _submission(flow, journal, state_key, state):
    problem_id = state['problem_id']
    widget_id = problem_id + ('-independent' if state.get('independent_followup') else '')
    draft_key = 'tools-submission:' + problem_id + (':independent' if state.get('independent_followup') else '')
    draft = journal.get('drafts', draft_key, {})
    def persist():
        journal.put('drafts', draft_key, {field:st.session_state.get('tools-' + widget_id + '-' + field, '')
            for field in ('how', 'sources', 'evidence', 'results', 'explanation', 'changed_input', 'changed_expected')})
    st.markdown('**How did you solve it?**')
    values = {}
    for field, label in [('how','Describe your approach'), ('sources','Help used: none, Copilot, Codex, ChatGPT, documentation or other sources'),
                         ('evidence','Relevant code / file contents'), ('results','Actual results and tests you ran'),
                         ('explanation','Reasoning, edge cases or questions (optional)')]:
        values[field] = st.text_area(label, value=draft.get(field, ''),
            key='tools-' + widget_id + '-' + field, on_change=persist)
    changed_input = changed_expected = ''
    if state.get('independent_followup') and flow.independent_problem(problem_id).get('needs_chosen_input'):
        changed_input = st.text_area('Exact changed input chosen before implementation',value=draft.get('changed_input',''),key='tools-'+widget_id+'-changed_input',on_change=persist)
        changed_expected = st.text_area('Exact expected result for that changed input',value=draft.get('changed_expected',''),key='tools-'+widget_id+'-changed_expected',on_change=persist)
    if st.button('Submit implementation for verification', key='tools-submit'):
        try:
            sources = [s.strip() for s in values['sources'].split(',') if s.strip()]
            if not sources:
                raise ValueError('Name the help you used, or enter none. Help is welcome and tracked separately.')
            saved = flow.submit(problem_id, how_solved=values['how'], assistance_sources=sources,
                evidence=values['evidence'], results=values['results'], explanation=values['explanation'],
                token='tools-' + uuid.uuid4().hex, independent_followup=bool(state.get('independent_followup')),
                diagnostic=bool(state.get('diagnostic')),changed_input=changed_input,changed_expected=changed_expected)
            state['submission_open'] = False
            journal.put('drafts', state_key, state)
            st.session_state['tools-message'] = 'Implementation saved locally. ' + ('Acceptance verified.' if saved.get('correct') is True else 'Review the implementation and acceptance evidence before completion.')
            st.rerun()
        except ValueError as error:
            st.error(str(error))
