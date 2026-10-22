"""Read-only Markdown sections and safe in-app links, never executable content."""
from pathlib import Path
import re
from urllib.parse import unquote, urlsplit
from services.routing import app_url


def headings(text):
    found, stack, fence = [], [], None
    lines = text.splitlines(keepends=True)
    for i, line in enumerate(lines):
        marker = re.match(r'^\s*(`{3,}|~{3,})', line)
        if marker:
            fence = None if fence == marker[1][0] else marker[1][0] if fence is None else fence
        m = re.match(r'^(#{1,6})\s+(.+?)\s*#*\s*$', line) if fence is None and not marker else None
        if m:
            level, label = len(m[1]), m[2]
            stack = [(n,h) for n,h in stack if n < level] + [(level,label)]
            found.append({'key':' / '.join(h for _,h in stack), 'label':label,'line':i,'level':level})
    return found


def section(text, key):
    entries = headings(text)
    entry = next((h for h in entries if h['key'] == key or h['label'] == key), None)
    if not entry:
        return text
    end = next((h['line'] for h in entries if h['line'] > entry['line'] and h['level'] <= entry['level']), len(text.splitlines()))
    return ''.join(text.splitlines(keepends=True)[entry['line']:end])


def render_links(records, path, text):
    def destination(value):
        parsed = urlsplit(value)
        if parsed.scheme or parsed.netloc:
            return value if parsed.scheme in ('http','https','mailto') else None
        target = unquote(parsed.path)
        if not target:
            return app_url('Notes Browser', note=path, heading=unquote(parsed.fragment))
        candidate = (Path(path).parent / target).as_posix()
        if not Path(target).suffix:
            # Obsidian vault-relative links may omit .md.
            candidate = 'Notes/' + target + '.md'
        try:
            real = records.path(candidate, notes_only=True)
            return app_url('Notes Browser', note=real.relative_to(records.root).as_posix(), heading=unquote(parsed.fragment) or None)
        except ValueError:
            # Repository evidence links are shown as text instead of inventing app routes.
            return None
    output, fence = [], None
    for line in text.splitlines(keepends=True):
        marker = re.match(r'^\s*(`{3,}|~{3,})', line)
        if marker:
            fence = None if fence == marker[1][0] else marker[1][0] if fence is None else fence
        if fence or marker:
            output.append(line)
            continue
        def markdown(m):
            url = destination(m[2])
            return f'[{m[1]}]({url})' if url else f'{m[1]} (`{m[2]}`)'
        line = re.sub(r'(?<!!)\[([^\]]+)\]\(([^)]+)\)', markdown, line)
        def wiki(m):
            target, _, label = m[1].partition('|')
            url = destination(target)
            return f'[{label or target}]({url})' if url else label or target
        line = re.sub(r'(?<!!)\[\[([^\]]+)\]\]', wiki, line)
        output.append(line)
    return ''.join(output)


def relationships(records, path):
    topics = [t for t in records.json('tracking/topic-map.json')['topics'] if any(s['path'] == path for s in t.get('sources', [])) or any(s['path'] == path for s in t.get('note_sections', []))]
    ids = {t['id'] for t in topics}
    mistakes = [m for m in records.json('tracking/mistakes.json')['mistakes'] if ids.intersection(m['topic_ids'])]
    exercises = sorted({e for t in topics for e in t['exercise_ids']})
    return topics, mistakes, exercises


def blocks(records, path, text):
    """Render local raster images without interpreting images inside code fences."""
    buffer, fence = [], None
    for line in text.splitlines(keepends=True):
        marker = re.match(r'^\s*(`{3,}|~{3,})',line)
        if marker:
            fence = None if fence == marker[1][0] else marker[1][0] if fence is None else fence
        image = (re.fullmatch(r'\s*!\[[^\]]*\]\(([^)]+)\)\s*',line) or re.fullmatch(r'\s*!\[\[([^\]]+)\]\]\s*',line)) if not fence and not marker else None
        if not image:
            buffer.append(line); continue
        if buffer:
            yield 'markdown',''.join(buffer); buffer=[]
        target = unquote(image[1].split('|')[0])
        try:
            asset = records.path((Path(path).parent/target).as_posix())
            if not asset.is_relative_to(records.root/'Notes') or asset.suffix.lower() not in ('.png','.jpg','.jpeg','.webp','.gif'):
                raise ValueError('Unsupported image')
            yield 'image',str(asset)
        except ValueError:
            matches = [p for p in (records.root/'Notes').rglob(Path(target).name) if p.is_file() and p.suffix.lower() in ('.png','.jpg','.jpeg','.webp','.gif') and p.resolve().is_relative_to(records.root/'Notes')]
            yield ('image',str(matches[0])) if len(matches)==1 else ('caption','Embedded file unavailable: '+target)
    if buffer:
        yield 'markdown',''.join(buffer)
