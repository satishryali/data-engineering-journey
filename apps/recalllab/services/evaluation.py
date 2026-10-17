"""Evaluation provenance: executable tests or explicitly labelled human evidence."""


def manual_assessment(original, reviewer, verification, feedback, score):
    if not reviewer.strip() or not verification.strip() or not feedback.strip():
        raise ValueError('Reviewer, observed verification/output, and feedback are required.')
    if type(score) is not int or score not in range(4):
        raise ValueError('Choose a rubric score from 0 to 3.')
    unaided = original.get('help_used') is False and original.get('notes_used') is False and original.get('hints_used') == 0
    assisted = original.get('help_used') is True or original.get('notes_used') is True or bool(original.get('hints_used'))
    # A reviewer cannot erase assistance/unknowns or manufacture independent retention.
    effective_score = score if unaided or score < 2 else 1 if assisted else None
    result = ('independent' if unaided else 'assisted' if assisted else 'unknown') if score >= 2 else 'needs_guidance'
    return {'score':effective_score,'result':result,'correct':True if score == 3 else False if score < 2 else None,
            'feedback':feedback,'evaluation':'human_review',
            'evaluation_status':'correct_independent' if score == 3 and unaided else 'correct_assisted' if score == 3 and assisted else 'correct_help_unknown' if score == 3 else 'partially_correct' if score in (1,2) else 'failed',
            'manual_assessment':{'reviewer':reviewer,'verification':verification,'requested_score':score,'provenance':'Human report; not executed by RecallLab'}}


def sql_assessment(tests, help_used, notes_used=False, hints=0):
    assisted = help_used is True or notes_used or hints > 0
    independent = help_used is False and not notes_used and not hints
    passed = tests['passed']
    partial = not passed and any(f['passed'] for f in tests['fixtures'])
    return {'score':(3 if independent else 1 if assisted else None) if passed else 1 if partial else 0,
            'result':('independent' if independent else 'assisted' if assisted else 'unknown') if passed else 'needs_guidance',
            'correct':passed,'evaluation':'sql_fixtures','test_evidence':tests,
            'evaluation_status':('correct_independent' if independent else 'correct_assisted' if assisted else 'correct_help_unknown') if passed else 'partially_correct' if partial else 'failed_tests',
            'feedback':('All controlled output fixtures passed. Explanation remains separately assessed.' if passed else
                        f'{sum(f["passed"] for f in tests["fixtures"])}/3 fixtures passed. Compare actual and expected rows; preserve customer identity, unmatched rows and NULL behaviour. '+(tests.get('error') or ''))}
