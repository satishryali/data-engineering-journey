"""Real Chromium visual smoke checks; run only against a disposable app instance.

Start the app with RECALLLAB_ROOT/RECALLLAB_DATA pointing at a scratch checkout,
then run: python apps/recalllab/tests/browser_redesign.py --url http://127.0.0.1:8502
Requires optional playwright and its Chromium browser, not production dependencies.
"""
import argparse
import json
from pathlib import Path
import re
import sys
from urllib.parse import urlencode
from playwright.sync_api import sync_playwright

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from services.routing import PAGES


def settled(page):
    page.wait_for_function("document.querySelector('[data-testid=stApp]')?.getAttribute('data-test-script-state') === 'notRunning'", timeout=30000)
    page.wait_for_timeout(600)  # Streamlit hydrates deferred widgets after script completion.


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--url', default='http://127.0.0.1:8502')
    parser.add_argument('--output', default='apps/recalllab/screenshots')
    args = parser.parse_args()
    output = Path(args.output)
    output.mkdir(parents=True, exist_ok=True)
    results = []
    with sync_playwright() as p:
        browser = p.chromium.launch()
        for size, width, height in [('desktop',1440,1000),('mobile',390,844)]:
            page = browser.new_page(viewport={'width':width,'height':height},reduced_motion='reduce')
            for route in PAGES:
                page.goto(args.url+'/?'+urlencode({'view':route}))
                heading = 'Make room for what stays.' if route == 'Dashboard' else route
                page.get_by_role('heading', name=heading, exact=True).wait_for(timeout=30000)
                settled(page)
                assert not page.locator('[data-testid=stException]').count(), route
                overflow = page.evaluate('document.documentElement.scrollWidth > innerWidth')
                assert not overflow, f'{size}: {route} overflows viewport'
                if route == 'Dashboard':
                    cta = page.get_by_role('link',name="Start Today's Revision",exact=True)
                    assert cta.is_visible()
                    bounds = cta.bounding_box()
                    assert bounds['y']+bounds['height'] < height, (size, bounds)
                    assert page.locator('.heatmap .day').count() == 365
                slug = re.sub('[^a-z0-9]+','-',route.lower()).strip('-')
                page.screenshot(path=str(output/f'{slug}-{size}.png'))
                results.append({'page':route,'viewport':size,'exception':False,'horizontal_overflow':overflow})
            page.close()
        browser.close()
    (output/'browser-results.json').write_text(json.dumps(results,indent=2),encoding='utf-8')
    print(f'{len(results)} page/viewport checks passed; screenshots in {output}')


if __name__ == '__main__':
    main()
