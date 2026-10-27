# Learning notes — Obsidian vault

Open this `Notes` folder directly as a vault in Obsidian. Do not open the whole
learning repository as the vault, and do not create another `Notes` folder inside it.

- [AI reminder model notes](AI/reminder-model-basics.md)
- [AI notes](AI/Index.md)
- [Python notes](Python/Index.md)
- [New syntax collection](New%20Syntax/README.md)
- [Revision records](revision/README.md)
- [Learning plan](learning-and-revision-plan.md)
- [SQL learning notes](SQL/learning-notes.md)
- [Recall questions, without answers](revision/questions.md)
- [Mistake index](revision/mistakes.md)

The five-role coach uses this vault for explanations, but the repository's tracking
CSV/JSON files own scheduling, mistake observations and progress evidence. Revision
JSON/JSONL and the mistake index here are generated views, not another editable tracker.
See [revision workflow](revision/README.md). Save learning records at checkpoint boundaries;
ordinary answers stay conversational. Timer events are recorded immediately.

## Use on another computer

1. Clone or update `satishryali/data-engineering-journey` using Git.
2. In Obsidian, choose **Open folder as vault** and select this checkout's `Notes` folder.
3. Work on one computer at a time. Before switching, review and commit your intended
   changes and push them. On the other computer, check for local changes and pull
   with `git pull --ff-only` before editing.

Obsidian reads and writes these local Markdown files directly. Git synchronizes them
only when you commit, push and pull; it does not provide continuous automatic sync.
The same Obsidian/Codex account does not replace these Git steps. In Codex, still use
the repository root for study commands and checkpoints; this vault is the notes area.

## Settings and credentials

Only the portable main, appearance and core-plugin preferences are tracked.
Device workspace state, community plugin files, plugin configuration, trash and
temporary files are ignored. Authentication and sync credentials must stay local.
Community plugins must be installed/configured separately on each computer if needed.

The migration consolidated the former nested copy into this folder. The former
Remotely Save configuration was archived locally rather than activated here;
Git is the intended transfer workflow for this vault. The old OneDrive vault was
left intact. Use this vault for new edits so the two copies do not diverge.

The Vault token in the teaching example is now a placeholder. Supply real tokens
through your local environment/secret store and never commit them in notes.

- [Notes-driven revision plan](revision/plan.md): upcoming dates, initial slots and coverage.
