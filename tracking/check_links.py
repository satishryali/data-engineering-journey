"""Check repository-local Markdown file/heading links without network requests."""
import argparse
from pathlib import Path
import re
import subprocess
from urllib.parse import unquote, urlsplit

ROOT = Path(__file__).resolve().parents[1]


def prose(text):
    lines, fence = [], None
    for line in text.splitlines():
        match = re.match(r'^\s*(`{3,}|~{3,})', line)
        if match:
            token = match[1][0]
            fence = None if fence == token else token
            continue
        if fence is None:
            lines.append(line)
    return '\n'.join(lines)


def headings(path):
    anchors, seen = set(), {}
    for line in prose(path.read_text(encoding='utf-8-sig')).splitlines():
        match = re.match(r'^#{1,6}\s+(.+?)\s*#*$', line)
        if match:
            slug = re.sub(r'[^\w\- ]', '', match[1].lower()).replace(' ', '-')
            n = seen.get(slug, 0)
            seen[slug] = n + 1
            anchors.add(f'{slug}-{n}' if n else slug)
    return anchors


def check(paths, root=ROOT):
    errors, count = [], 0
    vault_files = list((root / 'Notes').rglob('*'))
    for relative in paths:
        path = root / relative
        if not path.is_file() or path.suffix != '.md':
            continue
        content = prose(path.read_text(encoding='utf-8-sig'))
        links = re.findall(r'\]\((<[^>]+>|(?:[^()\s]|\([^()]*\))+)(?:\s+"[^"]*")?\)', content)
        links += re.findall(r'^\s*\[[^]]+\]:\s*(\S+)', content, re.MULTILINE)
        for link in links:
            target = re.sub(r'\\([()])', r'\1', unquote(link.strip('<>')))
            url = urlsplit(target)
            if url.scheme or url.netloc:
                continue
            count += 1
            file = (path.parent / url.path).resolve() if url.path else path
            if not file.exists():
                errors.append(f'{relative}: missing {target}')
            elif url.fragment and file.suffix == '.md':
                if url.fragment not in headings(file) and f'id="{url.fragment}"' not in file.read_text(encoding='utf-8-sig'):
                    errors.append(f'{relative}: missing heading {target}')
        for link in re.findall(r'\[\[([^]]+)\]\]', content):
            target = unquote(link.split('|')[0].split('#')[0])
            if not target:
                continue
            count += 1
            if not any(p.is_file() and (p.stem == target or p.name == target or p.as_posix().endswith('/'+target) or p.as_posix().endswith('/'+target+'.md')) for p in vault_files):
                errors.append(f'{relative}: missing vault link {target}')
    return count, errors


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--changed', action='store_true')
    args = parser.parse_args()
    paths = subprocess.check_output(['git', 'ls-files', '--cached', '--others', '--exclude-standard', '--', '*.md'], cwd=ROOT, text=True).splitlines()
    if args.changed:
        changed = set(subprocess.check_output(['git', 'diff', '--name-only', 'HEAD'], cwd=ROOT, text=True).splitlines())
        untracked = set(subprocess.check_output(['git', 'ls-files', '--others', '--exclude-standard'], cwd=ROOT, text=True).splitlines())
        paths = [p for p in paths if p in changed | untracked]
    count, errors = check(paths)
    print(f'Checked {count} local Markdown/vault links in {len(paths)} files; {len(errors)} unresolved.')
    print('\n'.join(errors))
    raise SystemExit(bool(errors))
