# Concurrency recall questions

Choose one bounded task before opening the explanation notes. State any notes or help used. These questions are unanswered and unscored.

1. Explain Python versus CPython versus C. With `ThreadPoolExecutor(max_workers=2)`, compare two waiting API calls with two large arithmetic loops. Who manages the GIL? Why can both API results appear together?
2. With `ProcessPoolExecutor(max_workers=2)`, explain what exists besides the main process. Which Python executable do spawned workers normally use when the main script starts with `.venv` Python? Distinguish installed packages from process memory.
3. Build two small async tasks that simulate waiting. Predict calling an async function without awaiting it, two sequential awaits, and running both through `gather`. Run both waiting arrangements and explain the actual output and timing.
4. In the saved two-shop example, explain why both `response ready` messages appear around ten seconds but both order strings appear around twenty seconds. State where each task resumes after its two `await` lines.
5. Given a weather API response, trace URL to JSON to `current.temperature_2m`. Explain the HTTP 400 result from requesting `temperature_2` and why the thread-pool error appears at `future.result()`.
6. Run two scheduled async functions with `await asyncio.sleep(2)`, then change only the wait to `time.sleep(2)`. Predict the message order and elapsed time for both runs. Explain why `async def` by itself does not make a blocking call yield.
7. Why use `urllib.parse.urlencode()` with a dictionary instead of typing `"?latitude=17.385&longitude=78.4867..."` by hand? What happens to spaces and the `&` symbol in a query parameter?

Explanation notes: [threads](../Python/Concepts/multithreading.md), [processes](../Python/Concepts/processes-and-gil.md), [async functions](../Python/Concepts/async-await.md), [API requests](../Python/Concepts/api-requests.md).
