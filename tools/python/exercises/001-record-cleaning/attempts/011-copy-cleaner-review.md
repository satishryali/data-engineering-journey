# Copying records - 16 October 2026

Earlier reviewed executions (transcribed because learner edited the same cell):
- Execution 112 called i.update with converted amount, appended i, and added reason directly to invalid i. Valid output integers and rejection reason were correct but input records were changed.
- Execution 115 set new_i = i, then called new_i.update and appended new_i. Tutor explained this is another name for the same dictionary, not a copy.
- Execution 126 used new_i = i.copy() before changing/appending it. Input display execution 129 still held changes from earlier runs. Tutor explained that copy does not undo old input mutations and supplied fresh input.
- Execution 131 recreated input with string amounts and no reasons; execution 132 displayed fresh input. Cleaner cell was not rerun afterward in saved notebook.

Tutor verification: executed saved fresh-input cell 32 followed by learner cleaner cell 28 in an isolated Python scope. Four valid amounts were integers [1200, 450, 350, 100]; one rejected record retained order_id 205, original bad amount and a reason. Compared input to a deep-copy baseline: unchanged. Checked output dictionaries were separate from every input dictionary. These are tutor-run results, not newly saved learner notebook outputs.

Help: diagnosis of input mutation; separate new-dictionary worked example; explanation of aliases; exact copy() hint; supplied fresh input and execution-order guidance. Correct with guidance, not independent or delayed retention. Blank/space-padded values and function/return remain untested.
