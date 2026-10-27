"""Tools command flow in a disposable journal; no synthetic canonical learning."""
import os
from pathlib import Path
import sys
import tempfile
import unittest
from unittest.mock import patch

APP = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(APP))
from streamlit.testing.v1 import AppTest
from services.journal import Journal
from services.curriculum import published_problems
from services.problems import Problems


class ToolsUITests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.journal_path = str(Path(self.temp.name) / 'tools.sqlite3')
        self.source = f'''import sys
sys.path.insert(0, {str(APP)!r})
from components.tools_ui import tools_page
from services.records import Records
from services.journal import Journal
tools_page(Records(), Journal({self.journal_path!r}))
'''

    def open(self):
        return AppTest.from_string(self.source, default_timeout=20).run()

    def command(self, app, command):
        app.text_input(key='tools-command').set_value(command)
        next(b for b in app.button if b.label == 'Send command').click().run()
        self.assertFalse(app.exception)

    def test_command_brief_and_draft_survive_restart_without_completion(self):
        app = self.open()
        self.assertFalse(app.exception)
        app.selectbox(key='tools-technology').set_value('python').run()
        self.command(app, '/problem')
        first = published_problems('python')[0]
        self.assertTrue(any(first['title'] == h.value for h in app.subheader))
        self.assertFalse(app.text_area)
        self.command(app, '/solved')
        self.assertEqual(len(app.text_area), 5)
        key = 'tools-' + first['id'] + '-how'
        app.text_area(key=key).set_value('Synthetic draft approach').run()
        restarted = self.open()
        self.assertFalse(restarted.exception)
        self.assertEqual(restarted.text_area(key=key).value, 'Synthetic draft approach')
        self.assertEqual(Journal(self.journal_path).attempts(), [])

    def test_submission_manual_review_and_next_are_evidence_driven(self):
        app = self.open()
        app.selectbox(key='tools-technology').set_value('python').run()
        self.command(app, '/problem')
        self.command(app, '/solved')
        first = published_problems('python')[0]
        for field, value in [('how', 'Read input and produce the required result'),
                             ('sources', 'ChatGPT'), ('evidence', '# Synthetic code submitted for UI test'),
                             ('results', 'Synthetic acceptance evidence, independently reviewed below')]:
            app.text_area(key='tools-' + first['id'] + '-' + field).set_value(value)
        next(b for b in app.button if b.label == 'Submit implementation for verification').click().run()
        self.assertFalse(app.exception)
        self.assertIsNone(Journal(self.journal_path).attempts()[0]['correct'])
        app.text_input(key='tools-reviewer').set_value('Test reviewer')
        app.text_area(key='tools-verification').set_value('Synthetic expected outputs and edge checks confirmed')
        app.text_area(key='tools-feedback').set_value('Synthetic feedback; no actual learner progress')
        next(s for s in app.selectbox if s.label == 'Review outcome').set_value(3)
        next(b for b in app.button if b.label == 'Save problem review').click().run()
        self.assertTrue(app.error)
        app.checkbox(key='tools-acceptance').check()
        next(b for b in app.button if b.label == 'Save problem review').click().run()
        self.assertFalse(app.exception)
        assessed = Journal(self.journal_path).effective_attempts()[0]
        self.assertTrue(assessed['correct'])
        self.assertEqual(assessed['result'], 'assisted')
        self.assertTrue(any('1 /' in m.value and 'problems completed' in m.value for m in app.markdown))
        self.assertTrue(any('Independent practice' in i.value for i in app.info))
        self.command(app, '/problem')
        self.assertTrue(any('Read several sales records' == h.value for h in app.subheader))

    def test_tools_is_an_existing_app_route(self):
        with patch.dict(os.environ, {'RECALLLAB_DATA': self.temp.name}):
            app = AppTest.from_file(str(APP / 'app.py'), default_timeout=30)
            app.query_params['view'] = 'Tools'
            app.run()
            self.assertFalse(app.exception)
            self.assertEqual(app.radio(key='route').value, 'Tools')

    def test_supported_commands_and_hints_preserve_assistance(self):
        app=self.open()
        app.selectbox(key='tools-technology').set_value('python').run()
        self.command(app,'/problem')
        first=published_problems('python')[0]
        self.command(app,'/hint')
        self.assertTrue(any(first['progressive_hints'][0] in n.value for n in app.info))
        self.command(app,'/stuck')
        self.assertTrue(any('smallest failing input' in n.value for n in app.info))
        self.command(app,'/why')
        self.assertTrue(any(first['engineering_relevance'] in n.value for n in app.info))
        self.command(app,'/progress')
        self.assertTrue(any('verified' in n.value and 'Current level' in n.value for n in app.info))
        self.command(app,'/review')
        self.assertTrue(any('No submitted implementation' in n.value for n in app.info))
        self.command(app,'/next')
        self.assertTrue(any(first['title']==s.value for s in app.subheader))
        self.assertEqual(Journal(self.journal_path).get('drafts','problem-help:'+first['id']+':initial')['hints_used'],2)

    def test_curated_pathway_does_not_require_full_bank(self):
        app=self.open()
        app.checkbox(key='tools-job-path').check().run()
        self.assertFalse(app.exception)
        self.assertTrue(any('full bank is not required' in c.value for c in app.caption))

    def test_failed_sql_shows_executed_actual_and_expected_without_progress(self):
        app = self.open()
        app.selectbox(key='tools-technology').set_value('sql').run()
        self.command(app, '/problem')
        self.command(app, '/solved')
        first = published_problems('sql')[0]
        for field, value in [('how', 'Synthetic deliberately incorrect SQL'), ('sources', 'none'),
                             ('evidence', 'SELECT 999'), ('results', 'One incorrect row')]:
            app.text_area(key='tools-' + first['id'] + '-' + field).set_value(value)
        next(b for b in app.button if b.label == 'Submit implementation for verification').click().run()
        self.assertFalse(app.exception)
        self.assertFalse(Journal(self.journal_path).attempts()[0]['correct'])
        self.assertTrue(any(e.label == 'Executed SQL fixture results' for e in app.expander))
        self.assertTrue(any('0 /' in m.value and 'problems completed' in m.value for m in app.markdown))

    def test_optional_existing_skill_assessment_opens_without_phantom_credit(self):
        app = self.open()
        app.selectbox(key='tools-technology').set_value('python').run()
        next(b for b in app.button if b.label == 'Open practical assessment').click().run()
        self.assertFalse(app.exception)
        diagnostic = Problems(Journal(self.journal_path)).acceleration_options('python')[0]
        self.assertTrue(any(h.value == diagnostic['title'] for h in app.subheader))
        self.assertEqual(Journal(self.journal_path).attempts(), [])
        self.command(app, '/solved')
        self.assertEqual(len(app.text_area), 5)

    def test_version_expansion_notice_requires_acknowledgement(self):
        journal = Journal(self.journal_path)
        journal.put('settings', 'tools-curriculum-version', {'version':'previous-test-version', 'totals':{'python':1}})
        journal.put('settings', 'tools-selected', 'python')
        app = self.open()
        self.assertTrue(any('1 →' in notice.value and 'preserved' in notice.value for notice in app.info))
        next(b for b in app.button if b.label == 'Acknowledge curriculum update').click().run()
        self.assertFalse(app.exception)
        self.assertFalse(any('Curriculum expanded:' in notice.value for notice in app.info))
        self.assertNotEqual(journal.get('settings', 'tools-curriculum-version')['version'], 'previous-test-version')

    def test_blocked_path_names_prerequisite_and_can_open_its_tool(self):
        app = self.open()
        app.selectbox(key='tools-technology').set_value('python').run()
        dependency = published_problems('sql')[0]['id']
        actual_published = published_problems
        def blocked(tool_id, curriculum=None):
            return [dict(actual_published(tool_id,curriculum)[0],id='TEST-BLOCKED',prerequisites=[dependency])] if tool_id == 'python' else actual_published(tool_id, curriculum)
        with patch('components.tools_ui.Problems.next_problem', return_value=None), patch('components.tools_ui.published_problems', side_effect=blocked):
            self.command(app, '/problem')
        self.assertTrue(any(dependency in notice.value for notice in app.info))
        self.assertFalse(any('future levels' in notice.value.lower() for notice in app.info))
        next(b for b in app.button if b.label == 'Practise prerequisite: SQL').click().run()
        self.assertFalse(app.exception)
        self.assertEqual(app.selectbox(key='tools-technology').value, 'sql')


if __name__ == '__main__':
    unittest.main()
