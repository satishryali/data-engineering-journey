"""Accessible native links keep the annual heatmap usable without injected scripts."""
from datetime import timedelta
from html import escape
from urllib.parse import urlencode
from services.records import level, metric_events
from services.routing import app_url

COLORS = ['#192536', '#9be9a8', '#68c87d', '#40a853', '#25863d', '#126329']


def heatmap(activity, metric, study=(.25, .5, 1, 1.25), attempts=(1, 3, 5, 8), page='Dashboard'):
    first, last = min(activity), max(activity)
    start = first - timedelta(days=first.weekday())
    weeks = (last - start).days // 7 + 1
    cells = []
    months = []
    for w in range(weeks):
        for row in range(7):
            d = start + timedelta(days=w * 7 + row)
            if d not in activity:
                continue
            v = activity[d]
            n = level((d, v), metric, study, attempts)
            if metric == 'All Learning':
                tip = f'{d}: {v["seconds"]/3600:.2f} confirmed study hours; {len(v["events"])} learning assessments; {len(v.get("revisions", []))} revision attempts'
            else:
                tip = f'{d}: {len(metric_events(v, metric))} {"revision attempts" if metric == "Revision Only" else "coding submissions"}; duration not measured'
            url = escape(app_url(page, day=d, metric=metric), quote=True)
            cells.append(f'<a target="_self" href="{url}" title="{escape(tip)}" aria-label="{escape(tip)}" style="grid-column:{w+2};grid-row:{row+2};background:{COLORS[n]}" class="day"></a>')
            if (d.day == 1 or d == first) and row < 7:
                months.append(f'<span style="grid-column:{w+2};grid-row:1">{d:%b}</span>')
    weekdays = ''.join(f'<span style="grid-column:1;grid-row:{i+2}">{name}</span>' for i, name in enumerate(['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']))
    legend = ''.join(f'<i style="background:{c}"></i>' for c in COLORS)
    return f'<div class="calendar-scroll"><div class="heatmap" style="--weeks:{weeks}">{weekdays}{"".join(months)}{"".join(cells)}</div></div><div class="legend">Less {legend} More</div>'
