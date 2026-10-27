# Collecting reminder inputs

Before building training examples, we need the task, time and repeat answer in a consistent form. The current collector asks for these three values.

## Read and clean text

The supplied script uses input() to read text and strip() to remove spaces at the beginning and end. Asking for a time in HH:MM format does not check that the entered value is a real time. Validation and saving examples are still future tasks.

The script currently prints task and time. It calls recurrence.upper() without saving or printing the returned text. No collector execution output was supplied.

## A string method returns new text

The practice notebook contains this small example:

```python
s = "satish"
s.upper()
```

Saved notebook result:

```text
'SATISH'
```

The next cell contains:

```python
print(s)
```

Saved notebook output:

```text
satish
```

upper() returns uppercase text. It does not replace the value held by s. A notebook can display the last expression's result; a script does not automatically print that expression. The shown output was read from saved notebook cells, not rerun during this note save.

## Sources and next step

- Project source: C:/GIT/AI/FineTuning/reminder_assistant/collect_example.py.
- Saved notebook: C:/GIT/AI/FineTuning/Test/reminder_assistant/collect_example_t.ipynb.
- [Exact pending task and session evidence](../../progress/ai-reminder/2026-10-28-session.md#exact-next-task).
- [Recall questions](recall-questions.md).

The learner writes the next change. No corrected collector, execution result or independent assessment is claimed here.
