# Cleaner functions and CSV reading - 16 October 2026

## Changed amounts and list reset

Blank string 301 rejected; space-padded 302 became integer 300; zero 303 became integer 0. First changed-data loop appended to earlier valid/rejected lists because the learner did not reset them. Tutor explained and prompted fresh lists. Saved executions 139-142 showed correct isolated results. Prediction/help report was not submitted. Source cell was subsequently edited; this paragraph preserves the actual reviewed outcome.

## Function attempts and corrections

Initial saved execution 152: def clean_orders(orders) looped over global test_payments, used external valid_orders/rejected_orders, and had no return. Tutor explicitly prompted moving list setup inside, looping over orders, returning both lists, and capturing returned values.

Execution 162 moved lists and return inside but still looped over test_payments. Tutor pointed out the remaining global variable, supplied exact replacement for i in orders, and gave the changed other_orders test. Execution 169 corrected definition. Changed record 401 amount string 75 returned integer 75 and no rejections (173-176).

Original dataset executions 177-181: valid IDs 101/102/105 amounts 500/200/300; rejected 103 bad and 104 blank retain originals and reasons. Displayed original orders retained all original strings and no added reason fields. Repeated-call test 182-187 kept first results and returned two empty lists for clean_orders([]).

These are guided successful implementation/application. No no-help reconstruction or delayed review was attempted. The original attempt.py remains historical; working implementation is in the notebook snapshot.

## CSV reading

Learner file files/orders.csv has header order_id,amount and five rows 501/250,502/bad,503/600,504/blank,505/0. Initial saved cells 192-207 used from csv import DictReader but called csv.DictReader; successful saved output could depend on prior kernel state. Tutor identified import/call mismatch, not a failure of CSV contents. Learner changed to import csv; executions 209-214 reran reading and cleaning successfully. CSV IDs remain strings; amount conversion only was required. with open and DictReader were used; independent explanation of resource closure was not assessed.

Valid IDs 501/503/505 have integer amounts 250/600/0. Rejected IDs 502/504 retain bad/blank values with reasons. Learner uses an absolute Windows path; future-machine path portability needs checking. No output CSV writing attempt has been reviewed.

## Help and next step

Known tutor guidance: list reset diagnosis; function local lists/parameter/return instructions; remaining parameter fix; changed dataset/tests; CSV DictReader concept and import correction. Learner did not report notes/other help or predictions; independence is not established. No duplicate score for prior copy-conversion corrections.

Next task: write valid_orders.csv (order_id,amount) and rejected_orders.csv (order_id,amount,reason) with csv.DictWriter, writeheader and writerows, using mode w and newline="". Read both back and display contents; leave original orders.csv unchanged. This was assigned, not completed.
