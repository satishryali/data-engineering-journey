# Error-handling practice - 16 October 2026

## Earlier reviewed attempt (notebook cell was later edited)

```python
total = 0
try:
    for i in test_payments:
        total += int(i['amount']) + total
except ValueError as e:
    print('The amount in the order_id : ', i['order_id'], 'is not a valid one. Please check')
print(total)
```

Observed saved execution 63: reported invalid order 205, then printed 6050. Tutor explained that += already includes the old total and that try/except outside the loop exits the loop at the first invalid value. This transcription preserves the reviewed attempt; it is not a proposed solution.

## Corrections and final output

Execution 67 fixed the double addition but kept try outside the loop, output 2000. Execution 68 placed try/except inside the loop, initially without a later valid record. Learner appended order 206 with amount string 100 (execution 69); final loop execution 71 reported invalid order 205 and printed 2100. Snapshot 009 preserves these later cells and output.

Known help: separate one-value try/except worked example, tutor diagnosis of both errors, loop/try indentation outline, repeated placement and valid-after-invalid reminders, run/save prompt. Final result is assisted correction, not independent or delayed retention. Prediction and explanation of why per-record handling continues were not submitted. The intentional earlier ValueError test is not a learner mistake.
