"""Published exercises remain readable through existing revision entry points."""
from datetime import date
from pathlib import Path
import sys
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from services.curriculum import published_problems
from services.questions import question
from services.records import Records
from services.sessions import varied_question


class PublishedRevisionCompatibility(unittest.TestCase):
    def test_registered_problem_needs_no_invented_note_concept(self):
        problem = published_problems('python')[0]
        q = question(Records(), problem['id'], date(2026, 10, 27))
        self.assertEqual(q.item_id, problem['id'])
        self.assertIn(problem['task'], q.prompt)
        self.assertIsNone(q.expected)
        self.assertEqual(q.sources, [])
        self.assertIn('Tools', q.prompt)

    def test_revision_formats_preserve_published_business_requirement(self):
        problem = published_problems('sql')[0]
        for style in ('coding', 'prediction', 'debug', 'explain'):
            task = varied_question(Records(), problem['id'], date(2026, 10, 27), style)
            self.assertIn(problem['task'], task['question']['prompt'])
            self.assertIsNone(task['runner'])
            self.assertIsNone(task['question']['expected'])


if __name__ == '__main__':
    unittest.main()
