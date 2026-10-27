"""Quality and publication audit of the existing bank; never invent missing content."""
from collections import Counter, defaultdict
import hashlib
import json
import re
from services.curriculum import validate_curriculum


TARGETS = {
    'Python for Data Engineering': ({'python'}, 450),
    'SQL and advanced SQL': ({'sql'}, 450),
    'PostgreSQL': ({'postgresql'}, 180),
    'PySpark and Spark SQL': ({'pyspark'}, 400),
    'Azure Data Factory': ({'adf'}, 350),
    'ADLS Gen2 and Azure Storage': ({'adls'}, 180),
    'Azure Databricks': ({'databricks'}, 250),
    'Delta Lake': ({'delta-lake'}, 150),
    'Data Modeling and ETL/ELT': ({'data-modelling', 'pipeline-reliability'}, 250),
    'Data Quality and Testing': ({'data-quality'}, 180),
    'Apache Airflow': ({'airflow'}, 180),
    'dbt': ({'dbt'}, 150),
    'Snowflake': ({'snowflake'}, 150),
    'Git, Linux and Docker': ({'git', 'shell', 'docker'}, 220),
    'Azure Fundamentals, Security and Monitoring': ({'azure', 'cloud-security'}, 180),
    'CI/CD and Deployment': ({'cicd'}, 130),
    'Integrated Pipeline Projects': ({'integrated-pipelines'}, 350),
}


def normalized(text):
    return re.sub(r'\s+', ' ', str(text).casefold()).strip()


def digest(value):
    return hashlib.sha256(json.dumps(value, sort_keys=True, ensure_ascii=False).encode()).hexdigest()


def audit(data):
    problems = data['problems']
    counts = Counter(p.get('tool_id') for p in problems)
    missing, duplicates, candidates = [], [], []
    identities, contracts, tasks = defaultdict(list), defaultdict(list), defaultdict(list)
    required = ('id', 'tool_id', 'title', 'scenario', 'learning_objective', 'inputs', 'expected_output',
                'acceptance_criteria', 'constraints', 'prerequisites', 'difficulty', 'level',
                'progressive_hints', 'engineering_relevance', 'estimated_minutes')
    for p in problems:
        for field in required:
            value = p.get(field)
            if value is None or (not value and field not in ('inputs', 'expected_output', 'prerequisites', 'level')):
                missing.append({'id': p.get('id'), 'field': field})
        if len(p.get('progressive_hints', [])) < 3:
            missing.append({'id': p.get('id'), 'field': 'three progressive hints'})
        identities[p.get('id')].append(p.get('tool_id'))
        contract = {k:p.get(k) for k in ('task','inputs','expected_output','acceptance_criteria','constraints')}
        contracts[digest(contract)].append(p.get('id'))
        # Near-duplicate candidates deliberately ignore names/numbers in the task.
        # Candidates require review; this audit cannot certify pedagogical meaning.
        task = normalized(p.get('task', ''))
        task = re.sub(r'\b\d+(?:\.\d+)?\b', '<number>', task)
        tasks[task].append(p)
    for ident, values in identities.items():
        if len(values)>1: duplicates.append({'kind':'stable_id', 'ids':[ident], 'count':len(values)})
    for ids in contracts.values():
        if len(ids)>1: duplicates.append({'kind':'identical_contract', 'ids':ids})
    for values in tasks.values():
        if len(values)>1:
            candidates.append({'ids':[p['id'] for p in values],
                               'transfer_labels':[p.get('challenge_kind') for p in values],
                               'reason':'Same task wording after numeric normalization; inspect changed technical constraints.'})
    by_id = {p['id']:p for p in problems}
    chosen_input_followups = [p['id'] for p in problems if not p.get('followup')
                              or p['followup'].get('inputs') == p.get('inputs')]
    pathway = data.get('job_ready_pathway', {})
    pathway_errors=[]
    for ident in pathway.get('problem_ids', []):
        if ident not in by_id: pathway_errors.append('Missing pathway problem: ' + ident)
        else:
            for dep in by_id[ident].get('prerequisites', []) + by_id[ident].get('independent_prerequisites', []):
                if dep not in pathway['problem_ids']: pathway_errors.append(f'{ident}: pathway omits prerequisite {dep}')
    for assessment in pathway.get('assessments', []):
        if assessment['problem_id'] not in pathway.get('problem_ids', []):
            pathway_errors.append('Assessment absent from pathway: ' + assessment['problem_id'])
    goals = [dict(track=name, technology_ids=sorted(tools), target=target,
                  published=sum(counts[t] for t in tools),
                  remaining=max(0,target-sum(counts[t] for t in tools))) for name,(tools,target) in TARGETS.items()]
    structure_errors = validate_curriculum(data)
    target_remaining = sum(row['remaining'] for row in goals)
    schema_valid = not (missing or duplicates or structure_errors or pathway_errors)
    quantity_complete = len(problems) >= 4200 and target_remaining == 0
    release = data.get('release_checks', {})
    return {'curriculum_version':data['version'], 'published_total':len(problems),
            'content_batches':data.get('content_batches', []),
            'draft_total':sum(b['draft'] for b in data.get('content_batches', [])),
            'independent_followups_requiring_learner_chosen_input':len(chosen_input_followups),
            'independent_followup_policy':'These problems require an exact new input and expected result supplied before implementation, then human review. This variant does not inflate published totals.',
            'target_total':4200, 'allocated_target_total':sum(r['target'] for r in goals),
            'target_note':'The requested numeric allocation totals 4,000. Integrated Pipeline Projects includes 200 additional bridge/transfer challenges.',
            'technology_counts':dict(sorted(counts.items())), 'track_counts':goals,
            'remaining_target_problems':target_remaining,
            'missing_fields':missing, 'duplicates':duplicates, 'similar_task_candidates':candidates,
            'broken_prerequisites_and_structure':structure_errors,
            'job_ready_pathway_errors':pathway_errors,
            'job_ready_pathway_count':len(pathway.get('problem_ids', [])),
            'schema_valid':schema_valid,
            'quantity_complete':quantity_complete,
            'release_checks':release,
            'pedagogical_quality':'Automated checks detect structural defects and duplicate candidates; they do not prove 4,200 meaningful pedagogical distinctions.',
            'acceptance_complete':bool(schema_valid and quantity_complete
                                       and release.get('app_tests_passed')
                                       and release.get('tracking_tests_passed')
                                       and release.get('coach_validation_passed')
                                       and release.get('specialist_content_review_recorded')
                                       and release.get('manual_review_limitation_disclosed'))}
