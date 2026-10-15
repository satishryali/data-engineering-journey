"""Install this repository's study commands globally. Requires Python 3.11+."""

import argparse
from datetime import datetime
import hashlib
import json
import os
from pathlib import Path
import re
import shutil
import tomllib


BEGIN = '# BEGIN data-engineering-journey study commands'
END = '# END data-engineering-journey study commands'
LEGACY = '# Personal study commands enabled; other installed skills disabled (reversible).'
NAMES = (
    'learning-coach', 'notes-keeper', 'mistake-keeper', 'revision-coach', 'progress-tracker',
    'github-agent',
    'start-timer', 'pause-timer', 'resume-timer', 'finish-study',
    'study-status', 'todays-schedule', 'save-checkpoint',
    'finish-for-today', 'continue-checkpoint',
)


def digest(data):
    return hashlib.sha256(data).hexdigest()


def remove_managed_block(text):
    if BEGIN in text or END in text:
        if text.count(BEGIN) != 1 or text.count(END) != 1:
            raise ValueError('Malformed managed config section; no changes made.')
        start, end = text.index(BEGIN), text.index(END) + len(END)
        if end < start:
            raise ValueError('Invalid managed config section; no changes made.')
        text = text[:start] + text[end:]
    # Migrate the earlier setup from this chat only when its tail contains
    # nothing except the exact path/enabled overrides that setup generated.
    if LEGACY in text:
        start = text.index(LEGACY)
        tail = text[start + len(LEGACY):]
        data = tomllib.loads(tail)
        entries = data.get('skills', {}).get('config', [])
        if set(data) != {'skills'} or any(set(e) != {'path', 'enabled'} for e in entries):
            raise ValueError('Legacy section has other settings; merge it manually.')
        text = text[:start]
    return text.rstrip() + '\n'


def install(repo, home, codex_home, keep_others=False, replace_existing=False):
    repo, home, codex_home = repo.resolve(), home.resolve(), codex_home.resolve()
    for rel in ('AGENTS.md', 'README.md', 'reference/study-tracking.md', 'tracking/study-log.csv'):
        if not (repo / rel).is_file():
            raise ValueError(f'Learning repository file missing: {rel}')
    target = home / '.agents' / 'skills'
    cfg = codex_home / 'config.toml'
    manifest = codex_home / 'study-commands-install.json'
    original = cfg.read_bytes() if cfg.exists() else b''
    base = remove_managed_block(original.decode('utf-8-sig'))
    parsed = tomllib.loads(base)
    prior = json.loads(manifest.read_text(encoding='utf-8')) if manifest.exists() else {}
    files = {}
    for name in NAMES:
        for rel in ('SKILL.md', 'agents/openai.yaml'):
            source = repo / 'codex' / 'skills' / name / rel
            content = source.read_text(encoding='utf-8')
            if rel == 'SKILL.md' and not re.search(r'^name: ' + re.escape(name) + r'\s*$', content, re.M):
                raise ValueError(f'Unexpected skill identity: {source}')
            content = content.replace('{{LEARNING_REPO}}', repo.as_posix())
            dest = target / name / rel
            data = content.encode('utf-8')
            if dest.exists() and dest.read_bytes() != data:
                owned = prior.get('files', {}).get(str(dest)) == digest(dest.read_bytes())
                if not owned and not replace_existing:
                    raise ValueError(f'Existing or edited command: {dest}. Review it first; '
                                     'use --replace-existing to back it up and replace it.')
            files[dest] = data

    desired = {(target / name / 'SKILL.md').as_posix(): True for name in NAMES}
    if not keep_others:
        for root in (target, codex_home / 'skills', codex_home / 'plugins' / 'cache'):
            if root.exists():
                for path in root.rglob('SKILL.md'):
                    if path not in files:
                        desired[path.as_posix()] = False

    # Preserve existing overrides, modifying only the enablement of a matching skill.
    existing_paths = set()
    pattern = r'(?ms)^\[\[skills\.config\]\][^\n]*\n.*?(?=^\[|\Z)'
    def merge(match):
        block = match.group(0)
        entry = tomllib.loads(block)['skills']['config'][0]
        path = str(entry.get('path', '')).replace('\\', '/')
        if path.endswith('/SKILL.md'):
            key = path
        else:
            key = path.rstrip('/') + '/SKILL.md'
        if key not in desired:
            return block
        existing_paths.add(key)
        value = 'true' if desired[key] else 'false'
        if re.search(r'^enabled\s*=', block, re.M):
            return re.sub(r'^enabled\s*=.*$', 'enabled = ' + value, block, flags=re.M)
        return block.rstrip() + '\nenabled = ' + value + '\n\n'
    base = re.sub(pattern, merge, base)
    block = '\n' + BEGIN + '\n'
    for path, enabled in sorted(desired.items()):
        if path not in existing_paths:
            block += '\n[[skills.config]]\npath = ' + json.dumps(path) + '\nenabled = ' + str(enabled).lower() + '\n'
    updated = (base.rstrip() + '\n' + block + '\n' + END + '\n').encode('utf-8')
    final = tomllib.loads(updated.decode('utf-8'))
    unrelated_before = {k: v for k, v in parsed.items() if k != 'skills'}
    unrelated_after = {k: v for k, v in final.items() if k != 'skills'}
    if unrelated_before != unrelated_after:
        raise ValueError('Unrelated settings changed; aborting.')

    changes = {p: data for p, data in files.items() if not p.exists() or p.read_bytes() != data}
    config_changed = updated != original
    backup = None
    if changes or config_changed:
        backup = codex_home / 'study-commands-backups' / datetime.now().strftime('%Y%m%d-%H%M%S-%f')
        backup.mkdir(parents=True, exist_ok=False)
        if cfg.exists():
            shutil.copy2(cfg, backup / 'config.toml')
        if manifest.exists():
            shutil.copy2(manifest, backup / manifest.name)
        for name in NAMES:
            directory = target / name
            if directory.exists() and any(p.is_relative_to(directory) for p in changes):
                shutil.copytree(directory, backup / 'skills' / name)
        if (cfg.read_bytes() if cfg.exists() else b'') != original:
            raise ValueError('Config changed concurrently; retry installation.')
        for path, data in changes.items():
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_bytes(data)
        if config_changed:
            cfg.parent.mkdir(parents=True, exist_ok=True)
            cfg.write_bytes(updated)
    manifest_data = {'repository': str(repo), 'files': {str(p): digest(data) for p, data in files.items()}}
    if not manifest.exists() or json.loads(manifest.read_text(encoding='utf-8')) != manifest_data:
        manifest.parent.mkdir(parents=True, exist_ok=True)
        manifest.write_text(json.dumps(manifest_data, indent=2) + '\n', encoding='utf-8')
    return {'commands': len(NAMES), 'changed_files': len(changes), 'config_changed': config_changed,
            'backup': str(backup) if backup else None, 'skills_folder': str(target)}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--keep-other-skills', action='store_true', help='Do not add disable overrides for other skills.')
    parser.add_argument('--replace-existing', action='store_true', help='Back up and replace conflicting personal command definitions.')
    args = parser.parse_args()
    try:
        result = install(Path(__file__).resolve().parents[1], Path.home(),
                         Path(os.environ.get('CODEX_HOME') or Path.home() / '.codex'),
                         args.keep_other_skills, args.replace_existing)
    except (OSError, ValueError) as error:
        parser.exit(1, f'{error}\n')
    print(json.dumps(result, indent=2))
    print('Restart Codex, then type / to find your study commands. Built-in commands remain.')
    print('No timer, checkpoint, credentials, or Git state was changed.')


if __name__ == '__main__':
    main()
