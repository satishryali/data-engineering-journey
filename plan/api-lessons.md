# API lessons for data engineering

Prepared at the learner's request on 3 November 2026. This is a lesson and practice
plan, not a record of completed learning. Follow the existing
[learning plan](learning-and-revision-plan.md) and [tutoring workflow](../reference/learning-coach.md).
RRDAP RDS-001 remains pending; these are separate practice tasks, not its solution.

## Resume point - 3 November 2026

Paused for SQL study at the learner's request. API-L01's introductory explanation was
given (client/server, URL parts, GET, headers, body and status). The order-request
exercise below is unanswered; no completion or independent understanding is claimed.
When returning, say **Resume API lesson 1** and attempt API-L01's request/response task.
No need to repeat the entire introduction unless wanted.

## Course goal

Read an unfamiliar API's documentation, fetch all required records, handle failures,
save data to PostgreSQL and run again safely. After that, build a small local API.

## How we will learn

- Work through one lesson at a time. A lesson can take more than one session.
- Each lesson starts with why it matters and a small explanation/example in conversation.
- Attempt one meaningful task, then share code, actual output and any notes/help used.
- The tutor reviews the attempt, gives focused hints if needed, then offers a changed task.
- Worked answers stay separate from practice. Attempt files are created when assigned,
  rather than filling the repository with future solution files.
- Explanations live in [Notes](../Notes/Python/Index.md). Extend the existing
  [API note](../Notes/Python/Concepts/api-requests.md) as lessons are actually taught.
- Existing weather practice and JSON notes are useful starting evidence, not proof that
  every API skill is independently demonstrated.
- Lesson IDs below identify curriculum only. Actual reviews, help and completion use
  the shared records at normal checkpoint boundaries; this is not a second tracker.
- Preparing/opening a lesson does not start a timer.

## Lesson sequence

| Lesson | Main goal | Prerequisite |
| --- | --- | --- |
| API-L01 | Understand a request and response | None |
| API-L02 | Make a Python GET request | L01; basic imports and variables |
| API-L03 | Extract and validate JSON records | L02; dictionaries and lists |
| API-L04 | Read documentation and choose HTTP methods | L03 |
| API-L05 | Use authentication safely | L04; environment variables introduced here |
| API-L06 | Collect every page | L03-L05; loops and functions |
| API-L07 | Handle HTTP, connection and data errors | L06; exceptions introduced/reviewed here |
| API-L08 | Respect rate limits and retry safely | L07 |
| API-L09 | Save raw data and create a clean file | L08; JSON/CSV files and paths |
| API-L10 | Load PostgreSQL and rerun safely | L09; SQL keys and database transactions |
| API-L11 | Build a small local API | L04 and L10; simple functions |
| API-L12 | Complete an unfamiliar ingestion challenge | L01-L10; L11 is a separate extension |

If a prerequisite is uncertain, use a small bridge task rather than restarting all Python.
Core ingestion scope is L01-L10 plus L12. L11 adds API building afterwards.

## API-L01: What happens when we call an API?

**Why:** Before writing code, be able to describe what one program asks another to do.

**We will cover:** API, client, server, HTTP/HTTPS, endpoint, method, path,
query parameters, headers, body and status code. Introduce REST as a common approach
to designing web APIs; API and REST are not interchangeable words.

**Task:** Inspect this fictional exchange. It is an offline example, not a real service.

```http
GET /orders?status=paid&limit=2 HTTP/1.1
Host: training.example
Accept: application/json
```

```http
HTTP/1.1 200 OK
Content-Type: application/json

{"orders":[{"id":101,"amount":250},{"id":102,"amount":400}]}
```

Submit one explanation identifying the client/server roles, method, host, path,
two query parameters, request and response headers, response status and response body.
Also write the request path/query you would use to ask for one pending order.

**Check:** Explain what changes in the request. Do not claim a live result or assume
the fictional service must return exactly the requested number of matching records.

**Changed task after feedback:** Interpret a different resource and an empty response list.

## API-L02: Fetch one response with Python

**Why:** Turn a documented URL into a useful Python response.

**We will cover:** A synchronous HTTP client, `requests.get`, `params`, `timeout`,
`status_code`, response headers, `raise_for_status`, `.text` and `.json()`.
Explain that decoding JSON and checking HTTP success are separate steps.

**Task:** Use the existing weather example and the provider's documentation to request
current temperature for one city. Supply parameters as a dictionary. Print the final
URL, status code, content type and parsed result type; then extract the temperature.
Use an explicit timeout and check HTTP status before treating the result as successful.

**Check:** Actual output is shown. Explain the difference between the response object,
its text body and the Python object returned by JSON decoding.

**Changed task:** Change the coordinates for another city without rewriting the request logic.

**Reading:** [Existing weather request note](../Notes/Python/Concepts/api-requests.md).
Check the selected interpreter/package availability before installation; no second
environment is required just for these lessons.

## API-L03: Read nested JSON and validate fields

**Why:** A successful request can still contain data your pipeline cannot use.

**We will cover:** Dictionaries/lists, nested access, missing versus null fields,
type checks, required fields and keeping rejected records with reasons.

**Offline input:**

```json
{"orders":[
  {"id":101,"customer":{"city":"Hyderabad"},"amount":"250.00"},
  {"id":102,"customer":{"city":null},"amount":"400.00"},
  {"id":103,"customer":{},"amount":"invalid"}
]}
```

**Task:** Produce records with `id`, `city` and a numeric amount. Define a missing-city
policy; reject invalid amounts with a reason while preserving the original record.
Do not change the input object. Use the existing Decimal note for money if needed.

**Check:** Report accepted/rejected counts, show their contents and explain your policy.
Expected check: three inputs are accounted for; valid money is preserved accurately.

**Changed task:** Add a missing ID and a zero amount; state the business rules before coding.

**Reading:** [JSON](../Notes/Python/Concepts/json.md),
[Decimal](../Notes/Python/Concepts/decimal-money.md).

## API-L04: Read documentation and choose methods

**Why:** Know what an API promises before deciding how to call it.

**We will cover:** Base URL, resource paths, path/query parameters, request bodies,
`GET`, `POST`, `PUT`, `PATCH`, `DELETE`, content types, API versions and common statuses
200, 201, 204, 400, 401, 403 and 404. Learn that the provider's documented contract matters.

**Task:** For a documented training API, describe how to read one order, filter orders,
create one order, change its status and delete it. Identify each method, path and
body if required. Run read-only calls first. Run mutations only against a local or
explicitly disposable sandbox, never a real business service.

**Check:** Explain which inputs belong in the path, query, headers and JSON body.
Handle a response with no body without blindly trying JSON decoding.

**Changed task:** Diagnose a wrong path separately from an invalid submitted field.

## API-L05: Authenticate without exposing secrets

**Why:** Many data sources require proof that your program may access them.

**We will cover:** API keys, bearer tokens, authentication versus authorization,
environment variables, expired credentials and introductory OAuth roles/token expiry.
Implementing an OAuth server is outside the initial scope.

**Task:** In a local test or disposable sandbox, read a dummy token from an environment
variable and send it where that API documents. Show behaviour for a missing token,
invalid token and accepted token. Use only dummy credentials for an echo endpoint.

**Check:** No secret in code, Git, screenshots or logs. Explain 401 versus 403 using
the test service's documented behaviour. An environment variable keeps secrets out of
source code but does not itself encrypt them or replace a production secret store.

**Changed task:** Replace the credential through configuration without editing the request function.

## API-L06: Collect all pages

**Why:** One response may be only part of the dataset.

**We will cover:** Page/offset and cursor pagination, page size, next links/tokens,
termination, empty pages and a stable-ID check. Do not invent pagination fields for an API.

**Task:** Begin with offline pages below, then use a documented paginated test source.
The tutor supplies its response contract before the attempt.

| Requested page | Order IDs returned | Next page |
| --- | --- | --- |
| 1 | 101, 102 | 2 |
| 2 | 103, 104 | 3 |
| 3 | 105 | null |

Collect every order into one result and record the pages requested.

**Check:** Expected fixture result: five distinct orders, pages 1-3 requested once,
and termination when the documented next value is null. Explain your stop condition.

**Changed task:** A later page repeats an ID; detect and report the overlap.
Discuss how changing source data affects pagination after the basic loop works.

## API-L07: Handle failures clearly

**Why:** A pipeline needs to distinguish request failure from bad returned data.

**We will cover:** Connection errors, timeouts, HTTP errors, invalid JSON, unexpected
response shape, useful exception boundaries and logs without secrets.

**Task:** Use controlled offline responses or a local test service covering success,
400, 401, 404, 500, a timeout and HTTP 200 with non-JSON content. Return or report a
clear outcome for each; preserve enough context to diagnose it.

**Check:** A failed page is never silently treated as an empty successful page.
Explain which step failed: connection, HTTP status, JSON decoding or record validation.
The tutor supplies a tiny fixture adapter if needed; learning a mocking framework is optional.

**Changed task:** A JSON response is valid but its expected record list is missing.

## API-L08: Rate limits and safe retries

**Why:** Recover from temporary trouble without overwhelming a source or repeating writes.

**We will cover:** 429, documented rate limits, `Retry-After`, increasing waits,
bounded attempts, timeouts, retryable failures and idempotency: whether repeating an
operation has the same intended effect. Automatic retry of arbitrary writes is unsafe.

**Task:** For a read-only fetch, simulate 429 then success, a temporary server failure
then success, a permanent 400 and repeated timeouts. Choose and explain a bounded retry
policy. Record waits using a test substitute rather than hitting a real service repeatedly.

**Check:** Transient cases recover; 400 stops; exhausted retries remain visible;
documented retry advice is respected. Logs show attempt counts without credentials.
Explain why a POST cannot automatically reuse the same retry policy.

**Changed task:** The service provides no retry header. Explain your fallback and upper bound.

## API-L09: Keep raw data and write a clean file

**Why:** Preserve received data for investigation while producing useful rows downstream.

**We will cover:** Raw versus cleaned data, JSON/CSV output, pathlib, UTC collection
timestamps, source metadata, rejection files and simple run summaries.

**Task:** Fetch or replay a small paginated dataset. Save the raw decoded page payloads
as JSON, accepted records as CSV and rejected records with reasons. Record the source
and collection time without secrets. Describe what your saved JSON preserves; a parsed
and re-encoded response is not a byte-for-byte network archive.

**Check:** Read the files back. Reconcile received, accepted and rejected counts;
show that a repeat run does not accidentally overwrite the previous raw run.

**Changed task:** A response gains an optional field; preserve it in raw JSON while
keeping the intended CSV columns stable.

## API-L10: Load PostgreSQL and rerun safely

**Why:** Turn an API extract into a verifiable, recoverable database load.

**We will cover:** Source IDs, database uniqueness, parameterized SQL, transactions,
insert/update rules, duplicate handling, incremental filters and a saved progress marker.
Use an isolated practice table, separate from RDS-001 and unrelated data.

**Task:** Load the five-order fixture from L06. Run it twice. Then load an updated
existing order plus one new order. Define the update rule and verify the results in SQL.
Finally, simulate a failure before commit and show how a retry behaves.

**Check:** Expected fixture counts: five after the initial and repeated loads; six
after one existing-order update and one new ID. Verify values as well as counts.
Demonstrate transaction behaviour and explain when a progress marker may advance.
For timestamp-based increments, discuss equal timestamps and boundary records.

**Changed task:** A later page fails; prove the next run can recover without losing records.
Introduce overlap windows or stronger source guarantees only when the fixture requires them.

## API-L11: Build a small local API

**Why:** Understand the server side after learning to consume APIs.

**We will cover:** FastAPI routes, path/query parameters, input validation, JSON request
bodies, response statuses, generated documentation and database access.

**Task:** Build an independent local practice service with `GET /orders`,
`GET /orders/{order_id}` and `POST /orders`. Start with a few synthetic in-memory orders,
then connect an isolated practice table after the route behaviour works.

**Check:** Demonstrate an existing/missing order, valid/invalid creation and a duplicate
ID policy. Call the local service from a separate client and inspect its documentation.
Label the in-memory version as temporary; restarting it does not prove persistence.

**Changed task:** Filter by status, then explain how you would distinguish PUT and PATCH.
Authentication deployment, multiple workers and production hosting are later topics.

## API-L12: Independent ingestion challenge

**Why:** Check whether the pieces work together on an unfamiliar source.

**Task:** The tutor selects a new documented API or supplies a deterministic local
contract with pagination, a stable ID and one controlled failure. Given the business
fields required, design and implement a small source-to-PostgreSQL job.
Select a source that permits the exercise; no paid subscription is required.

**Submit:** Approach, documentation used, code, actual outputs, redacted logs,
SQL verification and a clear account of help used.

**Check:** All required pages collected; invalid rows accounted for; secrets absent;
temporary failure handled with bounded retries; repeated runs avoid unintended
duplicates; an interrupted run can recover; source and stored counts reconcile.
Explain limitations of source ordering, updates and completeness where applicable.

**Changed task:** After feedback, reconstruct or modify one part with changed input.
Later retrieval uses the shared review schedule; immediate correction is not retention.
If substantial help was needed, record assisted work and arrange a fresh independent attempt.

## What can wait

GraphQL, gRPC, custom OAuth servers, API gateways, large microservice architectures,
high concurrency and public deployment. Async requests are an optional extension after
the synchronous ingestion path is correct and a measured need justifies concurrency.

## Sources and existing notes

References checked when preparing this plan; provider details must be checked again
when selecting a live exercise. Offline examples above are synthetic and not executed calls.

- [MDN: HTTP overview](https://developer.mozilla.org/en-US/docs/Web/HTTP/Guides/Overview)
- [Requests: quickstart](https://requests.readthedocs.io/en/latest/user/quickstart/)
- [FastAPI: tutorial](https://fastapi.tiangolo.com/tutorial/)
- [Weather request and URL parameters](../Notes/Python/Concepts/api-requests.md)
- [JSON conversion and files](../Notes/Python/Concepts/json.md)
- [Pathlib](../Notes/Python/Concepts/pathlib.md)
- [CSV writing](../Notes/Python/Concepts/csv-writing.md)
- [PostgreSQL connections](<../Notes/Python/Database Connections/postgres_connection.md>)
