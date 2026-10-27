"""Reviewed prompt corrections with stable published IDs and original hashes."""
from copy import deepcopy
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
BANK = ROOT/'tools/problem-bank'

TRANSFER_TASKS = {
 'RLP-PY-366': 'From the courier event, return only the literal ID as text. For a changed status value, verify the ID is unchanged; do not claim the status passed validation.',
 'RLP-PY-367': 'Return the courier status exactly as supplied. In a changed case, preserve the different spelling PICKED_UP rather than silently normalizing it.',
 'RLP-PY-368': 'Report the provider from its own field. Change the event ID in a second input and verify the provider is still taken from the provider field.',
 'RLP-PY-369': 'Return the envelope version separately from its nested event. Change the nested event ID and verify the envelope version remains 1.',
 'RLP-PY-370': 'Count courier event records, including the two supplied rows. Add one event with extra fields and verify the count becomes three, not the number of fields.',
 'RLP-PY-371': 'Report each event ID with its one-based arrival position. Reverse a changed input and show that positions change while event IDs remain the same.',
 'RLP-PY-372': 'Return the configured source filename exactly as text. Try a different filename without creating a file; a preview must not claim the path exists.',
 'RLP-PY-373': 'Report message MSG4 and delivery D9 as separate, labeled identifiers. Change only the nested delivery ID and verify the message ID stays MSG4.',
 'RLP-SQL-366': 'Count all three movement rows even though one note is NULL. Add a fourth row with a NULL note and verify the movement count increases to four.',
 'RLP-SQL-367': 'Count the two distinct SKUs in the three supplied movements. Add a new S3 movement and verify the distinct count becomes three while a repeated S1 does not increase it.',
}

def sha(value):
    return hashlib.sha256(json.dumps(value,sort_keys=True,separators=(',',':'),
                            ensure_ascii=False).encode('utf-8')).hexdigest()

def find(name, ident):
    body=json.loads((BANK/name).read_text(encoding='utf-8'))
    rows=body.get('problems') if isinstance(body,dict) else body
    return next(p for p in rows if p['id']==ident)

def make():
    proposals=[]
    for ident, task in TRANSFER_TASKS.items():
        name='python-batch5.json' if '-PY-' in ident else 'sql-batch5.json'
        original=find(name,ident)
        repaired=deepcopy(original)
        repaired['task']=task
        repaired['challenge_kind']='transfer'
        repaired['transfer_boundary']='Apply an earlier read/count skill to a courier or inventory contract with the specified changed-input check.'
        repaired['progressive_hints']=[
            'Write the exact output for the first supplied row before changing anything.',
            'Keep the field identity and the changed-input boundary separate: '+original['constraints'][0],
            'Compare the first and changed results, then explain which source value actually changed.']
        repaired['engineering_relevance']=(
            'A data-pipeline intake or reconciliation preview uses this result to trace a source record '
            'without claiming that unrelated validation has passed.')
        repaired['correction_reason']='Reviewed transfer labeling and focused task wording; stable ID and prerequisites.'
        proposals.append({'source_file':name,'original_published_id':ident,
                          'original_sha256':sha(original),'problem':repaired})

    original=find('dbt.json','RLP-DBT-002')
    dbt=deepcopy(original)
    dbt['scenario']='A distributor has a tiny approved training dbt project and needs to confirm that a supplied staging model produces both order rows.'
    dbt['task']='Copy the supplied seed and model into the existing isolated dbt project. Run the seed and only this model, then query the staging relation and show its actual rows and command results.'
    dbt['learning_objective']='Run a supplied two-row dbt seed/model and inspect the built relation.'
    dbt['inputs']={
        'environment':'An already configured dbt Core training project with a disposable database/schema and supported adapter. If unavailable, report environment_blocked; a plan is not an executed result.',
        'starter_files':{
            'seeds/orders_seed.csv':'order_id,amount\nO1,40.00\nO2,20.00\n',
            'models/stg_orders.sql':"select order_id, cast(amount as numeric(12,2)) as amount from {{ ref('orders_seed') }}\n"},
        'commands_to_run':['dbt seed --select orders_seed','dbt run --select stg_orders'],
    }
    dbt['expected_output']={'relation':'stg_orders','order_ids':['O1','O2'],
                            'row_count':2,'decimal_amounts':['40.00','20.00']}
    dbt['constraints']=[
        'Use only an isolated training target and the supplied synthetic seed.',
        'Keep project/profile credentials outside submitted code and output.',
        'Show actual adapter/version and command/query output; an unavailable target is not completion.']
    dbt['acceptance_criteria']=[
        'The seed and model commands finish in the isolated target; submit their actual results.',
        'Query stg_orders and show exactly O1 and O2 with their decimal amounts.',
        'A changed seed with O3 must remain a separate later independent exercise.',
        'Report all assistance; do not treat model SQL alone as proof of execution.']
    dbt['progressive_hints']=[
        'Check that the configured training project can see both supplied starter files.',
        'Run the seed first; the model reads that seed by its declared reference.',
        'If the run fails, compare the exact adapter error with the model and seed names before retrying.']
    dbt['engineering_relevance']='A small staging build verifies that a source seed is visible through dbt and that a downstream relation actually contains the contracted rows.'
    dbt['estimated_minutes']=25
    dbt['official_docs']=['https://docs.getdbt.com/docs/build/seeds',
                          'https://docs.getdbt.com/docs/build/models']
    dbt['followup']={
        'task':'With a changed seed that adds O3 amount 5.00, rerun the supplied staging model independently and verify all three rows.',
        'inputs':{'starter_files':dict(dbt['inputs']['starter_files'],
            **{'seeds/orders_seed.csv':'order_id,amount\nO1,40.00\nO2,20.00\nO3,5.00\n'})},
        'expected_output':{'order_ids':['O1','O2','O3'],'row_count':3},
        'verification':{'kind':'artifact_review'}}
    dbt['correction_reason']='Supplied model and seed artifacts were missing; focused beginner run contract added.'
    proposals.append({'source_file':'dbt.json','original_published_id':dbt['id'],
                      'original_sha256':sha(original),'problem':dbt})

    original=find('airflow.json','RLP-AIRFLOW-002')
    airflow=deepcopy(original)
    airflow['scenario']='A distributor uses an approved local Airflow training instance to make one courier delivery traceable by run and task log.'
    airflow['task']='Place the supplied single-task Airflow 3 DAG in the isolated training DAG folder, trigger it once, and find the task log for that exact run. Submit the run ID and observed log line.'
    airflow['learning_objective']='Trigger a supplied Airflow training DAG and locate the correct task log.'
    airflow['inputs']={
        'environment':'Existing authorized Airflow 3 training instance and isolated DAG folder. If access or supported version is unavailable, report environment_blocked; a pasted DAG is not execution evidence.',
        'starter_files':{'dags/training_delivery_log.py':(
            'import pendulum\n'
            'from airflow.sdk import dag, task\n\n'
            '@dag(dag_id="training_delivery_log", schedule=None,\n'
            '     start_date=pendulum.datetime(2026, 10, 20, tz="UTC"), catchup=False)\n'
            'def delivery_log():\n'
            '    @task()\n'
            '    def report():\n'
            '        print("delivery=D1 rows=1")\n'
            '    report()\n\n'
            'delivery_log()\n')},
        'dag_id':'training_delivery_log','task_id':'report',
    }
    airflow['expected_output']={'dag_id':'training_delivery_log','task_id':'report',
                                'task_log_contains':'delivery=D1 rows=1',
                                'run_id':'actual triggered run ID, supplied by observed Airflow output'}
    airflow['constraints']=[
        'Trigger only in the isolated training instance; no external notification or production run.',
        'Use the supplied source; the task is locating its actual run and log, not inventing a new DAG.',
        'If the installed Airflow version differs, record the version and use its official API or report environment_blocked.']
    airflow['acceptance_criteria']=[
        'The supplied DAG is discovered in the authorized training instance.',
        'One triggered run identifies task report and its actual run ID.',
        'The log from that run contains delivery=D1 rows=1; another run log does not substitute.',
        'Submit observed task state, log evidence and all assistance used.']
    airflow['progressive_hints']=[
        'Check the DAG ID and task ID in the supplied file before triggering.',
        'Use the triggered run ID to narrow the log lookup to one task instance.',
        'Compare the exact log line and task state with the expected result; preserve a failed run for review.']
    airflow['engineering_relevance']='Task-level logs tie an orchestrated batch outcome to a specific run, helping support staff investigate a failed or disputed delivery.'
    airflow['estimated_minutes']=25
    airflow['official_docs']=['https://airflow.apache.org/docs/apache-airflow/stable/tutorial/taskflow.html',
                              'https://airflow.apache.org/docs/apache-airflow/stable/tutorial/fundamentals.html']
    airflow['followup']={
        'task':'Run the same training DAG after changing the fixture line to delivery=D2 rows=0; locate the new run log independently.',
        'inputs':{'changed_log_line':'delivery=D2 rows=0','starter_dag':airflow['inputs']['starter_files']['dags/training_delivery_log.py']},
        'expected_output':{'task_log_contains':'delivery=D2 rows=0','run_id':'new observed run ID'},
        'verification':{'kind':'artifact_review'}}
    airflow['correction_reason']='Supplied DAG artifact was missing; focused log-lookup first success added.'
    proposals.append({'source_file':'airflow.json','original_published_id':airflow['id'],
                      'original_sha256':sha(original),'problem':airflow})
    return proposals

def main():
    proposals=make()
    wrapper={'schema_version':1,'status':'unregistered_corrections',
             'source_version':'2026.10.27.4','proposals':proposals,
             'review':'Stable-ID transfer labeling plus two executable starter-artifact repairs. Actual learner runs remain unverified.'}
    path=BANK/'reviewed-content-corrections.json'
    body=json.dumps(wrapper,indent=2,ensure_ascii=False)+'\n'
    path.write_text(body,encoding='utf-8')
    checkpoint={'status':'prepared_not_published','corrections':len(proposals),
                'source_sha256':hashlib.sha256(path.read_bytes()).hexdigest(),
                'ids':[p['original_published_id'] for p in proposals]}
    (BANK/'authors/reviewed-content-corrections-checkpoint.json').write_text(
        json.dumps(checkpoint,indent=2)+'\n',encoding='utf-8')
    print('Prepared',len(proposals),'stable-ID content corrections.')

if __name__=='__main__':
    main()
