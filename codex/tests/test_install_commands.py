import importlib.util
from pathlib import Path
import shutil
import tempfile
import tomllib
import unittest


REPO = Path(__file__).resolve().parents[2]
spec = importlib.util.spec_from_file_location('installer', REPO / 'codex/install_commands.py')
installer = importlib.util.module_from_spec(spec)
spec.loader.exec_module(installer)


class InstallerTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.base = Path(self.tmp.name)
        self.home = self.base / 'another user'
        self.codex = self.home / '.codex'
        self.codex.mkdir(parents=True)
        self.config = self.codex / 'config.toml'
        self.config.write_text('model = "existing-model"\n[plugins.example]\nenabled = true\n', encoding='utf-8')
        other = self.codex / 'plugins/cache/example/1/skills/other/SKILL.md'
        other.parent.mkdir(parents=True)
        other.write_text('---\nname: other\ndescription: Other skill\n---\n', encoding='utf-8')

    def run_install(self, repo=REPO, **kwargs):
        return installer.install(repo, self.home, self.codex, **kwargs)

    def test_install_preserves_settings_and_is_idempotent(self):
        result = self.run_install()
        self.assertEqual(result['commands'], 15)
        coach = self.home / '.agents/skills/learning-coach/SKILL.md'
        self.assertTrue(coach.is_file())
        self.assertIn('reference/learning-coach.md', coach.read_text(encoding='utf-8'))
        for role in ('learning-coach', 'notes-keeper', 'mistake-keeper', 'revision-coach', 'progress-tracker'):
            self.assertTrue((self.home / '.agents/skills' / role / 'agents/openai.yaml').is_file())
        github = self.home / '.agents/skills/github-agent'
        self.assertTrue((github / 'SKILL.md').is_file())
        self.assertIn('$github-agent', (github / 'agents/openai.yaml').read_text(encoding='utf-8'))
        data = tomllib.loads(self.config.read_text(encoding='utf-8'))
        self.assertEqual(data['model'], 'existing-model')
        self.assertTrue(data['plugins']['example']['enabled'])
        entries = data['skills']['config']
        self.assertEqual(sum(e['enabled'] for e in entries), 15)
        self.assertEqual(sum(not e['enabled'] for e in entries), 1)
        self.assertEqual((Path(result['backup']) / 'config.toml').read_text(),
                         'model = "existing-model"\n[plugins.example]\nenabled = true\n')
        self.assertEqual(self.run_install()['changed_files'], 0)
        self.assertFalse(self.run_install()['config_changed'])
        text = (self.home / '.agents/skills/start-timer/SKILL.md').read_text()
        self.assertIn(REPO.as_posix(), text)
        self.assertNotIn('{{LEARNING_REPO}}', text)

    def test_edited_skill_refused_then_backed_up_on_explicit_replace(self):
        self.run_install()
        skill = self.home / '.agents/skills/start-timer/SKILL.md'
        skill.write_text('my edited command', encoding='utf-8')
        before = self.config.read_bytes()
        with self.assertRaisesRegex(ValueError, 'Existing or edited'):
            self.run_install()
        self.assertEqual(self.config.read_bytes(), before)
        self.assertEqual(skill.read_text(), 'my edited command')
        result = self.run_install(replace_existing=True)
        saved = Path(result['backup']) / 'skills/start-timer/SKILL.md'
        self.assertEqual(saved.read_text(), 'my edited command')

    def test_new_checkout_path_and_keep_other_skills(self):
        self.run_install()
        moved = self.base / 'different checkout'
        shutil.copytree(REPO / 'codex', moved / 'codex', ignore=shutil.ignore_patterns('__pycache__'))
        for rel in ('AGENTS.md', 'README.md', 'reference/study-tracking.md', 'tracking/study-log.csv'):
            dest = moved / rel
            dest.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(REPO / rel, dest)
        self.run_install(repo=moved, keep_others=True)
        text = (self.home / '.agents/skills/start-timer/SKILL.md').read_text()
        self.assertIn(moved.as_posix(), text)
        self.assertNotIn(REPO.as_posix(), text)
        entries = tomllib.loads(self.config.read_text())['skills']['config']
        self.assertEqual(len(entries), 15)
        self.assertTrue(all(e['enabled'] for e in entries))

    def test_existing_override_merged_without_duplicate(self):
        path = (self.home / '.agents/skills/start-timer/SKILL.md').as_posix()
        with self.config.open('a', encoding='utf-8') as stream:
            stream.write('\n[[skills.config]]\npath = "' + path + '"\nenabled = false\n')
        self.run_install()
        entries = tomllib.loads(self.config.read_text())['skills']['config']
        matches = [e for e in entries if e['path'] == path]
        self.assertEqual(len(matches), 1)
        self.assertTrue(matches[0]['enabled'])


if __name__ == '__main__':
    unittest.main()
