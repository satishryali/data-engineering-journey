"""Validate and publish one batch in the existing RecallLab curriculum.

Only invoke after author files and promotion proposals are frozen. Rerunning the
same command is safe after an interrupted file-by-file publication. No learner
records, timers or services are touched.
"""
import argparse
from collections import Counter
from copy import deepcopy
import hashlib
import json
import os
from pathlib import Path
import sys
import tempfile

ROOT = Path(__file__).resolve().parents[1]
BANK = ROOT / 'tools/problem-bank'
BASE = ROOT / 'tools/curriculum.json'
sys.path.insert(0, str(ROOT / 'apps/recalllab'))
from services.curriculum import load_curriculum, published_problems
from services.bank_validation import audit


def read(path):
    return json.loads(path.read_text(encoding='utf-8'))


def exact_path(name):
    path = (BANK / name).resolve()
    if not path.is_relative_to(BANK.resolve()) or path.suffix != '.json' or not path.is_file():
        raise ValueError('Untrusted or missing bank file: ' + name)
    return path


def rows(value):
    value = value.get('problems') if isinstance(value, dict) else value
    if not isinstance(value, list):
        raise ValueError('Bank file must contain a problems array')
    return value


def digest(value):
    return hashlib.sha256(json.dumps(value, sort_keys=True, separators=(',', ':'),
        ensure_ascii=False).encode('utf-8')).hexdigest()


def stage_snapshot(data):
    totals = Counter(p['tool_id'] for p in data['problems'])
    for technology in data['technologies']:
        ident = technology['id']
        technology['published_total'] = totals[ident]
        for stage in technology['stages']:
            ids = [p['id'] for p in data['problems'] if p['tool_id'] == ident and p['level'] == stage['level']]
            stage.update(published_problem_ids=ids, status='published' if ids else 'planned')


def expanded_pathway(data):
    """A selected, dependency-closed January slice; it never requires all 4,200."""
    by_id = {p['id']:p for p in data['problems']}
    selected = set(data.get('job_ready_pathway', {}).get('problem_ids', []))
    for tool in ('python','sql','postgresql','pyspark','adf','adls','databricks',
                 'delta-lake','data-modelling','pipeline-reliability','data-quality','integrated-pipelines'):
        authored = published_problems(tool, data)
        for level in range(4):
            first = next((p for p in authored if p['level'] == level), None)
            if first:
                selected.add(first['id'])
    while True:
        before = len(selected)
        for ident in tuple(selected):
            problem = by_id[ident]
            selected.update(problem.get('prerequisites', []) + problem.get('independent_prerequisites', []))
        if len(selected) == before:
            break
    ordered = [p['id'] for p in data['problems'] if p['id'] in selected]
    data['job_ready_pathway']['problem_ids'] = ordered
    data['job_ready_pathway']['selection_policy'] = (
        'Curated first-success, bridge, business and quality tasks with complete prerequisite closure. '
        'The four assessments require their own demonstrated prerequisites, not completion of this whole pathway or bank.')


def atomic_write(path, content):
    handle, temporary = tempfile.mkstemp(prefix='.publish-', suffix='.tmp', dir=path.parent)
    try:
        with os.fdopen(handle, 'w', encoding='utf-8', newline='\n') as stream:
            stream.write(content)
            stream.flush()
            os.fsync(stream.fileno())
        os.replace(temporary, path)
    finally:
        if os.path.exists(temporary):
            os.unlink(temporary)


def publish(additions, promotions_name, version, dry_run=False, readability_name=None,
            snapshot_name=None, corrections_name=None):
    if snapshot_name:
        snapshot = read(exact_path(snapshot_name))
        if snapshot.get('version') != version:
            raise ValueError('Publication snapshot version differs from requested version')
        for name, expected in snapshot['file_sha256'].items():
            actual = hashlib.sha256(exact_path(name).read_bytes()).hexdigest()
            if actual != expected:
                raise ValueError('Frozen authoring file changed since QA: '+name)
    raw = read(BASE)
    data = load_curriculum(ROOT)
    current = {p['id']:p for p in data['problems']}
    changed_sources = {}
    source_roots = {Path(name).name for name in raw.get('problem_files', [])}
    promotion_count = 0
    proposal_names = [promotions_name] if isinstance(promotions_name, str) else list(promotions_name or [])
    for proposal_name in proposal_names:
        proposal = read(exact_path(proposal_name))
        if proposal.get('publication_status') != 'unregistered_proposals':
            raise ValueError('Promotion file is not marked as an unregistered proposal')
        for entry in proposal['proposals']:
            name = entry['source_file']
            if name not in source_roots:
                raise ValueError('Promotion source is not registered: ' + name)
            if name not in changed_sources:
                changed_sources[name] = read(exact_path(name))
            source = changed_sources[name]
            original = next((p for p in rows(source) if p['id'] == entry['original_draft_id']), None)
            replacement = deepcopy(entry['problem'])
            if not original or replacement['id'] != original['id'] or replacement.get('publication_status') != 'published':
                raise ValueError('Invalid promoted draft identity: ' + entry['original_draft_id'])
            if original.get('publication_status') == 'draft':
                if digest(original) != entry['original_draft_sha256']:
                    raise ValueError('Draft changed since authoring: ' + original['id'])
                replacement['published_version'] = version
                rows(source)[rows(source).index(original)] = replacement
                promotion_count += 1
            elif original != replacement and {k:v for k,v in original.items() if k!='published_version'} != {k:v for k,v in replacement.items() if k!='published_version'}:
                raise ValueError('Previously published row differs from proposal: ' + original['id'])
            if original['id'] in current and current[original['id']] != original:
                raise ValueError('Published identity conflict: ' + original['id'])
            current[replacement['id']] = replacement
    correction_count = 0
    if corrections_name:
        corrections = read(exact_path(corrections_name))
        if corrections.get('status') != 'unregistered_corrections':
            raise ValueError('Corrections file is not a pending review proposal')
        for entry in corrections['proposals']:
            name, ident = entry['source_file'], entry['original_published_id']
            if name not in source_roots:
                raise ValueError('Correction source is not registered: '+name)
            if name not in changed_sources:
                changed_sources[name] = read(exact_path(name))
            source = changed_sources[name]
            original = next((p for p in rows(source) if p['id'] == ident), None)
            replacement = deepcopy(entry['problem'])
            if not original or original.get('publication_status','published') != 'published':
                raise ValueError('Correction requires a published original: '+ident)
            if replacement.get('id') != ident or replacement.get('tool_id') != original.get('tool_id'):
                raise ValueError('Correction identity differs: '+ident)
            if replacement.get('level') != original.get('level') or replacement.get('prerequisites') != original.get('prerequisites'):
                raise ValueError('Correction changed level or prerequisite identity: '+ident)
            if digest(original) == entry['original_sha256']:
                replacement['published_version'] = version
                rows(source)[rows(source).index(original)] = replacement
                correction_count += 1
            elif {k:v for k,v in original.items() if k!='published_version'} != {k:v for k,v in replacement.items() if k!='published_version'}:
                raise ValueError('Correction source changed since review: '+ident)
            current[ident] = replacement
    readability_count = 0
    if readability_name:
        wording = read(exact_path(readability_name))
        if wording.get('status') != 'proposal_only_not_applied':
            raise ValueError('Readability file is not an unregistered proposal')
        source_for = {p['id']:name for name in source_roots
                      for p in rows(read(exact_path(name)))}
        for item in wording['items']:
            ident, field, old, revised = (item[k] for k in ('id','field','old','revised'))
            name = source_for.get(ident)
            if not name:
                raise ValueError('Unknown readability problem: '+ident)
            if name not in changed_sources:
                changed_sources[name] = read(exact_path(name))
            source = changed_sources[name]
            problem = next(p for p in rows(source) if p['id'] == ident)
            target = problem
            parts = field.split('.')
            for key in parts[:-1]:
                target = target[key]
            if target[parts[-1]] == old:
                target[parts[-1]] = revised
                readability_count += 1
            elif target[parts[-1]] != revised:
                raise ValueError('Readability source changed: '+ident+' / '+field)
            # Identical old prose can also appear in the displayed acceptance
            # checks. Keep those mirrors readable without changing numeric data.
            for collection in ('acceptance_criteria','progressive_hints'):
                problem[collection] = [line.replace(old,revised) if isinstance(line,str) else line
                                       for line in problem.get(collection,[])]
            if ident in current:
                current[ident] = problem
    appended = []
    for name in additions:
        path = exact_path(name)
        relative = path.relative_to(ROOT).as_posix()
        if relative in appended:
            raise ValueError('Duplicate add-file argument: ' + name)
        appended.append(relative)
        for problem in rows(read(path)):
            if problem.get('publication_status', 'published') != 'published':
                continue
            if problem['id'] in current and current[problem['id']] != problem:
                raise ValueError('Problem ID collision: ' + problem['id'])
            current[problem['id']] = problem
    proposed = deepcopy(data)
    proposed['problems'] = list(current.values())
    proposed['version'] = version
    stage_snapshot(proposed)
    expanded_pathway(proposed)
    report = audit(proposed)
    if not report['schema_valid'] or report['similar_task_candidates']:
        raise ValueError('Publication audit failed: ' + json.dumps({
            'missing':report['missing_fields'][:3], 'duplicates':report['duplicates'][:3],
            'structure':report['broken_prerequisites_and_structure'][:3],
            'similar':report['similar_task_candidates'][:3],
            'pathway':report['job_ready_pathway_errors'][:3]}))
    if dry_run:
        return {'published_after':len(proposed['problems']), 'promotions':promotion_count,
                'content_corrections':correction_count,
                'readability_corrections':readability_count,'files':appended,
                'version':version,'validated':True,'dry_run':True}
    for name, source in changed_sources.items():
        atomic_write(exact_path(name), json.dumps(source, indent=2, ensure_ascii=False)+'\n')
    for relative in appended:
        if relative not in raw['problem_files']:
            raw['problem_files'].append(relative)
    raw['version'] = version
    raw['technologies'] = proposed['technologies']
    raw['published_count'] = len(proposed['problems'])
    raw['publication_status'] = 'partial_expansion_target_unmet' if not report['quantity_complete'] else 'published_target_met'
    raw['job_ready_pathway'] = proposed['job_ready_pathway']
    atomic_write(BASE, json.dumps(raw, indent=2, ensure_ascii=False)+'\n')
    final = audit(load_curriculum(ROOT))
    destination = BANK / 'manifest.json'
    atomic_write(destination, json.dumps(final, indent=2, ensure_ascii=False)+'\n')
    return {'published_after':final['published_total'],'drafts':final['draft_total'],
            'promotions':promotion_count,'content_corrections':correction_count,
            'readability_corrections':readability_count,
            'files':appended,'version':version,
            'validated':final['schema_valid'],'quantity_complete':final['quantity_complete']}


if __name__=='__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--add-file', action='append', default=[], metavar='NAME.json')
    parser.add_argument('--promotions', action='append', default=[], metavar='NAME.json')
    parser.add_argument('--readability', metavar='NAME.json')
    parser.add_argument('--corrections', metavar='NAME.json')
    parser.add_argument('--snapshot', metavar='NAME.json',
                        help='Frozen source-file hashes from final authoring QA')
    parser.add_argument('--version', required=True)
    parser.add_argument('--dry-run', action='store_true')
    args = parser.parse_args()
    try:
        print(json.dumps(publish(args.add_file,args.promotions,args.version,
                                args.dry_run,args.readability,args.snapshot,
                                args.corrections),indent=2))
    except (KeyError, OSError, ValueError) as error:
        parser.exit(1,str(error)+'\n')
