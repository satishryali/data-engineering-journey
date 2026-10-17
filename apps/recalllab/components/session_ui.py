"""Integrated daily revision over a persistent, bounded, source-grounded plan."""
import hashlib
import streamlit as st
from services.questions import Question, evaluate
from services.sessions import get_plan, varied_question
from services.sql_runner import run_sql
from services.evaluation import sql_assessment
from components.assessment_ui import manual_review


def daily_session(records,journal,today,settings,note_view,recommendations,session_summary):
    session = journal.session()
    existing_plan = journal.get('settings','plan:'+session,{})
    budget = st.slider('Revision budget (minutes)',5,60,min(60,int(existing_plan.get('budget_minutes',settings['session_minutes']))),step=5,key='daily-budget-'+session)
    plan = get_plan(records,journal,session,budget,today)
    st.caption(f'Saved session · {plan["date_ist"]} · planned {sum(t["minutes"] for t in plan["tasks"])} minutes. No study timer is started. Resume this plan until completion; a new session uses current evidence and new variants.')
    attempts = journal.effective_attempts(session)
    done = {a.get('task_variant') for a in attempts}
    tasks = plan['tasks']
    completed = sum(t['question']['variant_id'] in done for t in tasks)
    st.progress(completed/len(tasks),text=f'{completed} / {len(tasks)} planned tasks submitted')
    cursor_key = 'cursor:'+session
    cursor = journal.get('settings',cursor_key,0)
    ids = list(range(len(tasks)))
    def persist_cursor():
        journal.put('settings',cursor_key,st.session_state['daily-task-'+session])
    chosen = st.selectbox("Today's task",ids,index=None if 'daily-task-'+session in st.session_state else min(cursor,len(tasks)-1),format_func=lambda i:f'{i+1}. {tasks[i]["question"]["title"]} · {tasks[i]["question"]["mode"]} · {tasks[i]["minutes"]} min',key='daily-task-'+session,on_change=persist_cursor)
    task = tasks[chosen]
    q = Question(**task['question'])
    render_task(records,journal,session,q,task.get('runner'),note_view,recommendations)
    current = next((a for a in journal.effective_attempts(session) if a.get('task_variant')==q.variant_id),None)
    if current and chosen+1 < len(tasks):
        def advance():
            journal.put('settings',cursor_key,chosen+1)
            st.session_state['daily-task-'+session] = chosen+1
        st.button('Next Task',type='primary',on_click=advance)
    if completed == len(tasks):
        st.success('All planned tasks submitted. Review unevaluated answers below, then complete the session to save the canonical checkpoint.')
    manual_review(journal,session,'daily-manual')
    session_summary()


def render_task(records,journal,session,q,runner,note_view,recommendations):
    token = session+':daily:'+q.variant_id
    draft = journal.get('drafts',token,{})
    answer_key = 'daily-answer-'+token
    explanation_key = 'daily-explanation-'+token
    if answer_key not in st.session_state:
        st.session_state[answer_key] = draft.get('answer','')
        st.session_state[explanation_key] = draft.get('explanation','')
    def persist():
        journal.put('drafts',token,dict(journal.get('drafts',token,{}),answer=st.session_state.get(answer_key,''),explanation=st.session_state.get(explanation_key,''),question=q.dict()))
    st.subheader(q.title)
    st.caption(q.mode+' · '+q.variant_id)
    st.markdown(q.prompt)
    if q.mode=='Python coding':
        st.info('Python Run Tests is disabled until a verified isolated runner exists. Save your code and verification for the human-review workflow below.')
    answer = st.text_area('Your answer / code (JSON for output prediction)',key=answer_key,height=210,on_change=persist)
    explanation = st.text_area('Reasoning / manual verification output',key=explanation_key,on_change=persist)
    if runner and st.button('Run Query',key='run-'+token):
        tests = run_sql(answer,runner)
        journal.put('drafts',token,dict(journal.get('drafts',token,{}),tests=tests,tested_hash=hashlib.sha256(answer.encode()).hexdigest()))
        st.rerun()
    draft = journal.get('drafts',token,{})
    tests = draft.get('tests') if draft.get('tested_hash')==hashlib.sha256(answer.encode()).hexdigest() else None
    if tests:
        st.success('All controlled fixtures passed') if tests['passed'] else st.warning('Some or all controlled fixtures failed')
        st.json(tests)
    hints = draft.get('hints',0)
    if st.button('Next hint',key='hint-'+token,disabled=hints>=len(q.hints)):
        journal.put('drafts',token,dict(draft,hints=hints+1)); st.rerun()
    for hint in q.hints[:hints]:
        st.info(hint)
    if st.button('Consult source section',key='notes-'+token):
        journal.put('drafts',token,dict(draft,notes_used=True)); st.rerun()
    notes_used = draft.get('notes_used',False)
    if notes_used and q.sources:
        source = q.sources[0]
        with st.expander('Source section · assistance recorded',expanded=True):
            note_view(source['path'],source.get('key'))
    declaration_key = 'daily-help-'+token
    declaration = st.radio('Other help used?',['Unknown / not stated','No help','Yes'],key=declaration_key,horizontal=True,
                           index=['Unknown / not stated','No help','Yes'].index(draft.get('help','Unknown / not stated')))
    journal.put('drafts',token,dict(journal.get('drafts',token,{}),help=declaration))
    help_used = {'Unknown / not stated':None,'No help':False,'Yes':True}[declaration]
    if hints or notes_used:
        help_used = True
    if st.button('Submit Attempt',type='primary',key='submit-'+token):
        try:
            assessment = sql_assessment(tests,help_used,notes_used,hints) if tests else evaluate(q,answer,help_used,notes_used,hints)
            saved = journal.save(session,token,dict(item_id=q.item_id,question=q.prompt,answer=answer,explanation=explanation,
                task_variant=q.variant_id,sources=q.sources,dimension=q.dimension,hints_used=hints,notes_used=notes_used,
                help_used=help_used,practice_context='revision',assessment_kind='application',code_submission=bool(runner or q.mode=='Python coding'),**assessment))
            st.success('Saved locally / pending sync: '+saved['attempt_id'])
        except ValueError as error:
            st.error(str(error))
    saved = next((a for a in journal.effective_attempts(session) if a.get('task_variant')==q.variant_id),None)
    if saved:
        st.write(saved['feedback'])
        st.caption('Evaluation: '+saved.get('evaluation_status',saved['evaluation'])+' · score '+str(saved.get('score')))
        if st.button('Show worked reference',key='reference-'+token):
            journal.put('drafts',token,dict(journal.get('drafts',token,{}),reference_open=True)); st.rerun()
        if draft.get('reference_open'):
            st.write(q.solution)
        recommendations(journal.effective_attempts(session),'daily-task')
        ai = journal.get('settings','local-ai',{})
        if ai.get('enabled'):
            with st.expander('Optional local AI explanation · unverified'):
                st.caption('Sends this submitted question/answer and its first source section to your configured local Ollama process only. It cannot change scores or claim tests passed.')
                if st.button('Ask local explanation',key='ai-'+token):
                    from services.ai import explain
                    from services.notes import section
                    source = q.sources[0] if q.sources else None
                    text = section(records.path(source['path']).read_text(encoding='utf-8-sig'),source.get('key','')) if source else ''
                    response = explain(ai['endpoint'],ai['model'],text,q.prompt,answer,opted_in=True)
                    journal.put('settings','ai:'+saved['attempt_id'],response)
                response = journal.get('settings','ai:'+saved['attempt_id'])
                if response:
                    st.write(response)
