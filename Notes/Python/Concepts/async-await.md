# Normal and async functions

Async functions let a program handle other tasks while waiting for things such as API responses. Several waits can overlap on one thread.

## Calling def and async def

A normal `def` function runs its body when called. Calling an `async def` function creates a **coroutine object**: an object representing work that can run and pause. Calling it alone does not run its body or schedule a task.

```python
import asyncio

def normal_order():
    return "O-1"

async def async_order():
    return "O-2"

async def main():
    print(normal_order())
    pending = async_order()
    print("Coroutine created; its body has not run yet")
    print(await pending)

asyncio.run(main())
```

Expected output:

```text
O-1
Coroutine created; its body has not run yet
O-2
```

- `await pending` runs the coroutine and waits for its result.
- `asyncio.run(main())` starts an **event loop**, which manages async tasks, and runs `main` in a normal script.
- In a notebook with an event loop already running, use `await main()` instead of `asyncio.run(main())`.
- A coroutine is distinct from a scheduled task. `asyncio.gather()` below schedules the supplied coroutines so their waits can overlap.

## Two overlapping waits

Goal: receive two order results while their waits overlap. `asyncio.sleep()` simulates waiting; no API request is made.

```python
import asyncio
from time import perf_counter

async def fetch_order(order_id):
    await asyncio.sleep(1)
    return f"{order_id}: received"

async def main():
    start = perf_counter()
    results = await asyncio.gather(
        fetch_order("O-1"),
        fetch_order("O-2"),
    )
    print(results)
    print(f"Elapsed: {perf_counter() - start:.2f} seconds")

asyncio.run(main())
```

Expected output: these results, with elapsed time about 1 second plus overhead.

```text
['O-1: received', 'O-2: received']
```

When a task reaches an `await` that needs to wait, it gives the event loop a chance to run another task. It resumes when the wait is ready. An `await` that is already ready need not pause.

Replace the `gather()` call with these lines inside `main` to wait one after the other, taking about 2 seconds:

```python
first = await fetch_order("O-1")
second = await fetch_order("O-2")
results = [first, second]
```

Writing `async def` alone does not make two calls run together.

## Two pauses in each shop

The saved notebook also scheduled Shop A and Shop B with `create_task()`. Each shop printed `request started`, awaited a ten-second sleep, printed `response ready`, awaited a **second** ten-second sleep, then returned its orders. The saved output took about 20.03 seconds: both shops' first waits overlapped, then both second waits overlapped.

Execution order: the notebook schedules A and B, then pauses at `print(await shop_a)` because A's result is not ready. A starts and pauses at its first `await`; B starts and pauses at its first `await`. At about ten seconds each resumes, prints `response ready`, and pauses at its own second `await`. At about twenty seconds each returns. Only then can the notebook print the returned order strings.

At an `await`, the task keeps its local values and its next position. After the first sleep it continues at `response ready`; after the second it continues at `return`. A print inside the coroutine happens when that task runs. `print(await shop_a)` belongs to the notebook code and happens only when the notebook resumes after A's result is ready. Another ready task may print first. The order of near-simultaneous resumes is not guaranteed.

## Compared with your thread pool

| Approach | While one API call waits |
| --- | --- |
| Normal functions with `ThreadPoolExecutor(max_workers=2)` | Another worker thread can execute |
| Async functions with an async HTTP client | Another scheduled task can execute on the same event-loop thread |

Async code needs operations that support async waiting. A normal blocking API client inside `async def` still blocks the event-loop thread. `time.sleep()` also blocks it; `await asyncio.sleep()` allows other tasks to run.

A long Python calculation inside an async function keeps the thread busy. `async` does not create another CPU core or make that calculation faster.

## Sources and learning context

Explained on 29 October 2026. Correction to the earlier chat wording: a coroutine object is distinct from a scheduled task.

Saved outputs in `practice/Sync/Async/async.ipynb` show sequential two-second async waits taking 4.02 seconds and `gather()` taking 2.00 seconds. A separate cell prints `coroutine` before its function starts. These saved outputs were inspected, not rerun. The tutor gave worked code and explanations in this session; no independent assessment is recorded. The timings are not guarantees.

- [Python coroutines, tasks and gather](https://docs.python.org/3.14/library/asyncio-task.html)
- [Normal functions](functions.md)
- [Threads and waiting](multithreading.md)
- [Recall questions](../../revision/concurrency-questions.md)
