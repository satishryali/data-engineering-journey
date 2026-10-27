"""Published practical problems. Planned stages never inflate completion totals.

This module is read-only: completion/assistance evidence belongs to Problems and
canonical checkpoint records, never to a curriculum manifest.
"""
from copy import deepcopy
from collections import Counter, deque
from functools import lru_cache
import json
import re
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[3]


@lru_cache(maxsize=4)
def _load_documents(signature):
    return {name: json.loads(Path(name).read_text(encoding='utf-8')) for name, stamp, size in signature}


def load_curriculum(repo_root=None):
    root = Path(repo_root) if repo_root is not None else REPO_ROOT
    manifest = root / 'tools/curriculum.json'
    base = json.loads(manifest.read_text(encoding='utf-8'))
    paths = [manifest]
    for relative in base.get('problem_files', []):
        path = (root / relative).resolve()
        if not path.is_relative_to((root / 'tools/problem-bank').resolve()) or path.suffix != '.json':
            raise ValueError('Invalid problem-bank path: ' + relative)
        if not path.is_file():
            raise ValueError('Missing published problem file: ' + relative)
        paths.append(path)
    metadata_path = root / 'tools/problem-bank/seed-metadata.json'
    if metadata_path.exists():
        paths.append(metadata_path)
    signature = tuple((str(p), p.stat().st_mtime_ns, p.stat().st_size) for p in paths)
    documents = _load_documents(signature)
    data = deepcopy(documents[str(manifest)])
    data['content_batches'] = []
    for path in paths[1:]:
        if path == metadata_path:
            metadata = documents[str(path)]
            for problem in data['problems']:
                problem.update(deepcopy(metadata.get(problem['id'], {})))
            continue
        batch = documents[str(path)]
        if isinstance(batch, dict) and isinstance(batch.get('problems'), list):
            batch = batch['problems']
        if not isinstance(batch, list):
            raise ValueError('Published problem file must contain an array or problems array: ' + str(path))
        published = [p for p in batch if p.get('publication_status', 'published') == 'published']
        data['content_batches'].append(dict(path=path.relative_to(root).as_posix(),authored=len(batch),published=len(published),draft=len(batch)-len(published)))
        data['problems'].extend(deepcopy(p) for p in published)
    totals = Counter(p['tool_id'] for p in data['problems'])
    for technology in data['technologies']:
        technology['published_total'] = totals[technology['id']]
        for stage in technology['stages']:
            ids = [p['id'] for p in data['problems'] if p['tool_id'] == technology['id'] and p['level'] == stage['level']]
            stage.update(published_problem_ids=ids, status='published' if ids else 'planned')
    return data


@lru_cache(maxsize=2)
def _cached_compiled(signature):
    return load_curriculum()


def cached_curriculum():
    """Shared read-only catalog for repeated page renders; source changes invalidate it."""
    manifest = REPO_ROOT / 'tools/curriculum.json'
    base = json.loads(manifest.read_text(encoding='utf-8'))
    paths = [manifest, REPO_ROOT/'tools/problem-bank/seed-metadata.json']
    paths.extend(REPO_ROOT/name for name in base.get('problem_files', []))
    signature = tuple((str(path),path.stat().st_mtime_ns,path.stat().st_size) for path in paths if path.exists())
    return _cached_compiled(signature)


def list_technologies(curriculum=None):
    return deepcopy((curriculum or load_curriculum())['technologies'])


def published_problems(tool_id, curriculum=None):
    problems = [p for p in (curriculum or load_curriculum())['problems'] if p['tool_id'] == tool_id]
    return deepcopy(sorted(problems, key=lambda p: (p['level'], p.get('sequence', 0), p['id'])))


def get_problem(problem_id, curriculum=None):
    return next((deepcopy(p) for p in (curriculum or load_curriculum())['problems'] if p['id'] == problem_id), None)


def diagnostic_problem(tool_id, curriculum=None):
    return next((p for p in published_problems(tool_id, curriculum) if p.get('diagnostic')), None)


def prerequisite_coverage(independent_ids=(), curriculum=None):
    independent = set(independent_ids)
    return {covered for p in (curriculum or load_curriculum())['problems']
            if p['id'] in independent and p.get('diagnostic')
            for covered in p.get('diagnostic_covers', [])}


def prerequisites_met(problem, verified_ids=(), independent_ids=(), curriculum=None):
    missing, missing_independent = missing_prerequisites(problem, verified_ids, independent_ids, curriculum)
    return not missing and not missing_independent


def missing_prerequisites(problem, verified_ids=(), independent_ids=(), curriculum=None,
                          *, _index=None, _coverage=None):
    """Include inherited requirements; an assisted diagnostic waives none of them."""
    data = curriculum or load_curriculum()
    by_id = _index if _index is not None else {p['id']:p for p in data['problems']}
    verified, independent = set(verified_ids), set(independent_ids)
    coverage = _coverage if _coverage is not None else prerequisite_coverage(verified & independent, data)
    satisfied = verified | coverage
    missing, missing_independent, visited = set(), set(), set()
    pending = list(problem.get('prerequisites', ())) + list(problem.get('independent_prerequisites', ()))
    while pending:
        ident = pending.pop()
        if ident in visited:
            continue
        visited.add(ident)
        if ident not in satisfied:
            missing.add(ident)
        parent = by_id.get(ident)
        if parent and ident not in coverage:
            pending.extend(parent.get('prerequisites', ()))
            pending.extend(parent.get('independent_prerequisites', ()))
            missing_independent.update(set(parent.get('independent_prerequisites', ())) - (independent | coverage))
    missing_independent.update(set(problem.get('independent_prerequisites', ())) - (independent | coverage))
    return missing, missing_independent


def select_next_problem(tool_id, verified_ids=(), independent_ids=(), curriculum=None, allowed_ids=None):
    verified = set(verified_ids)
    data = curriculum or load_curriculum()
    coverage = prerequisite_coverage(verified & set(independent_ids), data)
    index = {p['id']:p for p in data['problems']}
    problems = published_problems(tool_id, data)
    eligible = [p for p in problems if p['id'] not in (verified | coverage)
                and (allowed_ids is None or p['id'] in allowed_ids)
                and not any(missing_prerequisites(p, verified, independent_ids, data,
                                                  _index=index, _coverage=coverage))]
    if not eligible:
        return None
    # A learner who demonstrated one stage can attempt the next eligible stage
    # without clearing every parallel beginner task. Browse remains available for
    # optional breadth/revision; neither skipped task earns completion credit.
    highest = max((p['level'] for p in problems if p['id'] in verified), default=-1)
    if highest >= 0:
        next_stage = next((p for p in eligible if p['level'] == highest + 1), None)
        if next_stage:
            return next_stage
        same_stage = next((p for p in eligible if p['level'] == highest), None)
        if same_stage:
            return same_stage
    return eligible[0]


def pathway_status(verified_ids=(), independent_ids=(), curriculum=None):
    data = curriculum or load_curriculum()
    pathway = data.get('job_ready_pathway', {})
    by_id = {p['id']: p for p in data['problems']}
    ids = set(pathway.get('problem_ids', []))
    verified, independent = set(verified_ids), set(independent_ids)
    assessments = []
    for checkpoint in pathway.get('assessments', []):
        problem = by_id.get(checkpoint['problem_id'])
        assessments.append(dict(checkpoint, eligible=bool(problem and prerequisites_met(problem, verified, independent, data)),
                                completed=checkpoint['problem_id'] in verified,
                                independent=checkpoint['problem_id'] in independent))
    return dict(target_date=pathway.get('target_date'), total=len(ids),
                completed=len(ids & verified), independent=len(ids & independent), assessments=assessments)


def progress_counts(tool_id, verified_ids=(), independent_ids=(), curriculum=None):
    problems = published_problems(tool_id, curriculum)
    ids = {p['id'] for p in problems}
    verified = ids & set(verified_ids)
    independent = verified & set(independent_ids)
    nxt = select_next_problem(tool_id, verified_ids, independent_ids, curriculum)
    milestones = [n for n in range(10, len(ids) + 1, 10) if n <= len(verified)]
    return {'completed': len(verified), 'independent': len(independent), 'total': len(ids),
            'current_level': nxt['level'] if nxt else max((p['level'] for p in problems), default=0),
            'next_problem_number': next((i for i,p in enumerate(problems,1) if nxt and p['id'] == nxt['id']), None),
            'next_problem_id': nxt['id'] if nxt else None,
            'milestone': milestones[-1] if milestones else None,
            'curriculum_version': (curriculum or load_curriculum())['version']}


def overall_progress(verified_ids=(), independent_ids=(), curriculum=None):
    data = curriculum or load_curriculum()
    track = {t['id'] for t in data['technologies'] if t.get('job_ready_track')}
    ids = {p['id'] for p in data['problems'] if p['tool_id'] in track}
    done = ids & set(verified_ids)
    return {'completed': len(done), 'independent': len(done & set(independent_ids)), 'total': len(ids),
            'label': 'Published Job-Ready practice', 'curriculum_version': data['version'],
            'note': 'Practice completion is not a readiness percentage; assessments require independent evidence.'}


def learner_prompt(problem):
    """Only current task fields; no future stage, solution, verifier or hidden cases."""
    fields = ('id', 'tool_id', 'title', 'level', 'scenario', 'task', 'inputs',
              'expected_output', 'constraints', 'acceptance_criteria', 'estimated_minutes',
              'engineering_relevance', 'official_docs')
    return {key: deepcopy(problem[key]) for key in fields if key in problem}


def validate_curriculum(curriculum=None):
    data = curriculum or load_curriculum()
    errors = []
    technologies = data.get('technologies', [])
    tools = {t['id'] for t in technologies}
    problems = data.get('problems', [])
    by_id = {p['id']: p for p in problems if isinstance(p.get('id'), str)}
    if len(tools) != len(technologies): errors.append('Duplicate technology IDs')
    if len(by_id) != len(problems): errors.append('Duplicate problem IDs')
    required = ('id','tool_id','title','level','scenario','task','inputs','expected_output',
                'constraints','acceptance_criteria','estimated_minutes','engineering_relevance','official_docs','prerequisites')
    for t in technologies:
        if [s['level'] for s in t.get('stages', [])] != list(range(11)):
            errors.append(f"{t['id']}: stages must be exactly 0..10")
        if t.get('published_total') != sum(p['tool_id'] == t['id'] for p in problems):
            errors.append(f"{t['id']}: published total does not match actual problems")
    for p in problems:
        label = p.get('id', '<missing ID>')
        for field in required:
            if field not in p: errors.append(f"{label}: missing {field}")
        if p.get('tool_id') not in tools: errors.append(f"{label}: unknown technology")
        if type(p.get('level')) is not int or not 0 <= p['level'] <= 10: errors.append(f"{label}: invalid level")
        stamp = str(p.get('published_version', ''))
        version = str(data.get('version', ''))
        if re.fullmatch(r'\d{4}\.\d{1,2}\.\d{1,2}\.\d+',stamp) and re.fullmatch(r'\d{4}\.\d{1,2}\.\d{1,2}\.\d+',version):
            if tuple(map(int,stamp.split('.'))) > tuple(map(int,version.split('.'))):
                errors.append(f"{label}: published_version is newer than curriculum version")
        for dep in p.get('prerequisites', []) + p.get('independent_prerequisites', []) + p.get('diagnostic_covers', []):
            if dep not in by_id:
                errors.append(f"{p['id']}: unknown prerequisite {dep}")
            elif (dep not in p.get('diagnostic_covers', []) and by_id[dep].get('tool_id') == p.get('tool_id')
                  and type(p.get('level')) is int and type(by_id[dep].get('level')) is int):
                if p['level'] > by_id[dep]['level'] + 1:
                    errors.append(f"{p['id']}: missing difficulty bridge")
                if p['level'] < by_id[dep]['level']:
                    errors.append(f"{p['id']}: prerequisite is harder than the problem")
    # Kahn traversal also handles long curriculum chains without recursion limits.
    dependencies = {pid: set(p.get('prerequisites', []) + p.get('independent_prerequisites', [])) & by_id.keys() for pid,p in by_id.items()}
    dependents = {pid: [] for pid in by_id}
    for pid, deps in dependencies.items():
        for dep in deps: dependents[dep].append(pid)
    ready = deque(pid for pid,deps in dependencies.items() if not deps)
    visited = set()
    while ready:
        pid = ready.popleft()
        visited.add(pid)
        for child in dependents[pid]:
            dependencies[child].discard(pid)
            if not dependencies[child]: ready.append(child)
    if len(visited) != len(by_id): errors.append('cyclic prerequisites: ' + ', '.join(sorted(by_id.keys() - visited)[:20]))
    return errors
