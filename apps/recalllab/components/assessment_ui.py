"""Explicit manual review, never automatic execution or AI grading."""
import streamlit as st


def manual_review(journal, session, namespace='manual'):
    pending = [a for a in journal.effective_attempts(session) if a.get('evaluation') == 'manual_pending']
    if not pending:
        return
    with st.expander(f'Human assessment · {len(pending)} unevaluated submissions'):
        st.caption('A human reviewer checks code/output or reasoning. RecallLab does not run Python. Original help declarations and submitted source are preserved.')
        selected = st.selectbox('Submission to assess', pending,format_func=lambda a:a['item_id']+' · '+a['attempt_id'][-8:],key=namespace+'-attempt')
        st.markdown(selected['question'])
        st.code(selected['answer'])
        st.caption(f'Original help: {selected.get("help_used")!r}; notes: {selected.get("notes_used")!r}; hints: {selected.get("hints_used")!r}')
        with st.form(namespace+'-form'):
            reviewer = st.text_input('Reviewer name / role')
            verification = st.text_area('Observed output, edge-case checks or reasoning evidence')
            feedback = st.text_area('Specific feedback and next action')
            score = st.selectbox('Rubric score', [None,0,1,2,3],format_func=lambda s:{None:'Choose after reviewing',0:'0 — unable / major gap',1:'1 — partial / substantial guidance',2:'2 — independent but incomplete',3:'3 — correct with sound verification'}[s])
            attested = st.checkbox('I reviewed the actual submission and the evidence above; this is a human assessment.')
            if st.form_submit_button('Save human assessment'):
                try:
                    if not attested:
                        raise ValueError('A human must review and attest the actual evidence.')
                    journal.assess(selected['attempt_id'],dict(reviewer=reviewer,verification=verification,feedback=feedback,score=score))
                    st.success('Human assessment saved locally. It will enter canonical history at session completion.')
                    st.rerun()
                except ValueError as error:
                    st.error(str(error))
