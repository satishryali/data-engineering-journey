# The learner's note-writing style

Use the learner's existing Python dictionary and PostgreSQL connection notes as the
style reference. Keep their short headings, direct explanations and practical examples;
do not copy spelling errors or incorrect technical claims.

- Start with why we need the concept and what problem it solves, in one or two simple sentences.
- Use short headings such as Creating a list, Accessing items, or Method 1: using append.
- Write short bullets with one idea each. Use familiar words rather than formal terms.
- Explain a necessary technical word immediately: index means an item's position.
  Prefer "we can change the items" over introducing "mutable" without explanation.
- Explain one idea at a time, naturally, as if sitting beside the learner's computer.
- Add an example when it shows a different behaviour or clears up a real confusion.
  Do not repeat the same point just to increase the number of examples.
- Keep runnable examples small and complete. Label predicted output **Expected output**.
  Label it **Output verified by running** only after actually executing that code with
  the shown input. Never present predicted output as an execution result.
- Prefer orders, employees, CSV files and database records. Use other familiar data
  when it makes the explanation clearer. Connect
  examples to practical work without supplying a solution to an active learner exercise.
- Show a common mistake and its correction when useful. Explain what went wrong simply.
- Keep code names accurate, preserve useful existing wording, and check code/output.
- Put recall questions in a separate file; keep answers/examples in the explanation note.
- Keep source links and administrative details at the end. Do not put long tracking or
  assessment disclaimers ahead of the explanation the learner wants to read.
- Stay within the requested topic and current needs. More examples does not mean adding
  advanced material or writing a whole textbook. Notes do not imply assessed proficiency.

## How to explain code

1. State what we want to achieve and why.
2. Show a small input.
3. Show the code, including any setup needed to run it.
4. Show expected output, clearly distinguishing it from output actually run and checked.
5. Explain how the important lines produce that output. Do not narrate every character.
6. Add a useful variation or common mistake only when relevant.

Explain new syntax plainly. Use saved attempts and feedback to decide what has actually
been demonstrated; do not repeatedly explain syntax already understood independently.
If understanding is uncertain, do not invent either proficiency or a misconception.
Keep conditions and exceptions that matter: for example, valid integer strings can be
converted with int(), while an invalid value can raise ValueError. Define important
technical terms immediately. Mark installation commands as shell commands, not Python;
use Python code fences for Python inputs, even if a pasted style example used another label.

## Choose useful content, not a fixed checklist

Include only the sections that help this concept: why we need it, a simple explanation,
small examples/output, practical uses, actual learner doubts, important corrections,
a short recap, and a few separate recall questions. A simple idea can have a short note;
a genuine difficulty can need a longer explanation. Do not add empty or invented sections.

Capture only doubts the learner actually expressed. Link observed learner mistakes to
their stable IDs in tracking/mistakes.json through the generated vault index, instead
of copying the entire mistake history into the note. Keep source-note errors separate.
Distinguish **explained to the learner** from **demonstrated independently**, based on
actual saved evidence. Do not invent a successful attempt, duration or review result.

Inspect and update the relevant existing note before creating another one. Keep revision
questions separate from explanations/answers so the learner can try recall first.

## Applying a style change

Apply these preferences to future notes. Do not automatically rewrite the existing
vault. If the learner asks to check a style first, show one short sample based on the
current learning topic in conversation and wait for feedback before a broader rewrite.
The sample is a tutor explanation, not a learner attempt or evidence of mastery.
Keep the real pending exercise unchanged unless the learner changes it.

This is an explicit learner preference, recorded on 15 October 2026. Apply it to future
notes unless the learner requests another format. Existing notes need only targeted
updates unless a broader rewrite is requested.
