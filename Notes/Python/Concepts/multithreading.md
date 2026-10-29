# Multithreading

Multithreading lets Python handle tasks that spend time waiting—such as downloading files, calling APIs, or querying a database—without freezing the entire program. While one thread waits for data, another thread can keep running.

---

## Why we need multithreading

With one blocking call at a time, the next call waits. If an API request takes 3 seconds, that thread cannot start its next line until the request finishes.

Multithreading creates separate worker tracks inside the same program:
- **MainThread**: The default worker that starts when you run any Python script.
- **Worker Thread**: An extra worker created to run a specific task in the background.

While a worker thread waits on slow network or disk input/output (I/O), the MainThread stays active.

---

## Running a background task with `threading.Thread`

```python
import threading
import time

def slow_task():
    print(f"Inside task: running on {threading.current_thread().name}")
    time.sleep(3)
    print("Background work finished!")

print(f"Before start: {threading.current_thread().name}")

t = threading.Thread(target=slow_task)
t.start()

print(f"After start: {threading.current_thread().name}")
```

### Example output (order may vary)

```text
Before start: MainThread
Inside task: running on Thread-1 (slow_task)
After start: MainThread
Background work finished!
```

### How the important lines work:
- `target=slow_task`: Passes the function object itself without parentheses `()`.
- `t.start()`: Starts the worker thread. The main thread can continue without waiting for the worker's 3-second sleep. Which thread prints first can vary.
- `time.sleep(3)`: Pauses only the background worker. The operating system switches CPU attention to `MainThread`.

---

## Why `target=slow_task` has no parentheses `()`

- `slow_task()` (with parentheses) executes the function **immediately** on the current line and returns its result (usually `None`). Writing `target=slow_task()` freezes the main thread and passes `None` to the thread.
- `slow_task` (without parentheses) passes the **function object** (the recipe) to the thread. When `t.start()` runs, the new thread adds the parentheses and executes `slow_task()`.

---

## Waiting for results with `t.join()`

If your next line needs the data or file created by the background thread, the main thread must wait before proceeding. `t.join()` pauses the main thread until that background thread completes.

### Real data pipeline example: CSV copy and read-back

This pattern was tested with `amazon.csv` to ensure `amazon_v1.csv` is completely written before reading it:

```python
import threading
import csv

field_names = [
    'product_id', 'product_name', 'category', 'discounted_price',
    'actual_price', 'discount_percentage', 'rating', 'rating_count',
    'about_product', 'user_id', 'user_name', 'review_id',
    'review_title', 'review_content', 'img_link', 'product_link'
]

records = []

def load_and_export():
    print(f"Reading amazon.csv on: {threading.current_thread().name}")
    with open("amazon.csv", "r", encoding="utf-8", newline="") as f:
        reader = csv.DictReader(f)
        for row in reader:
            records.append(row)

    print(f"Writing amazon_v1.csv on: {threading.current_thread().name}")
    with open("amazon_v1.csv", "w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=field_names)
        writer.writeheader()
        writer.writerows(records)

# 1. Start loading in the background
t = threading.Thread(target=load_and_export)
t.start()

# 2. Wait until export finishes before attempting to read
t.join()

# 3. Safely read the generated file
with open("amazon_v1.csv", "r", encoding="utf-8", newline="") as f:
    reader = csv.reader(f)
    header = next(reader)
    print(f"Successfully read exported file. Columns: {len(header)}")
```

### Why `t.join()` matters here:
Without `t.join()`, the main thread might try opening `amazon_v1.csv` before the worker finishes writing. The result could be an error or incomplete data. `join()` waits for completion; it does not return the worker function's value.

---

## Managing multiple workers with `ThreadPoolExecutor`

When processing many files or API calls, creating threads manually with `threading.Thread` becomes repetitive. Python's `concurrent.futures.ThreadPoolExecutor` manages a pool of reusable workers:

```python
import time
from concurrent.futures import ThreadPoolExecutor

def fetch_table(table_name):
    print(f"Fetching {table_name}...")
    time.sleep(2)
    return f"{table_name}_data"

tables = ["users", "orders", "products"]

start = time.time()

with ThreadPoolExecutor(max_workers=3) as executor:
    results = list(executor.map(fetch_table, tables))

total_time = time.time() - start

print(f"Results: {results}")
print(f"Total time: {total_time:.2f} seconds")
```

### Expected output:
```text
Fetching users...
Fetching orders...
Fetching products...
Results: ['users_data', 'orders_data', 'products_data']
Total time: 2.00 seconds
```

Rather than taking about 6 seconds one after another, the three waits can overlap and finish in about 2 seconds. The exact time and print order vary.

- `max_workers=3` is the maximum number of jobs active in this pool at once. Extra submitted jobs wait for a free worker.
- `executor` is just the variable name for the pool. `submit(function, arguments)` is another way to give it a job.
- `submit()` returns a `Future`, a holder for a result that may arrive later. `future.result()` waits if needed and returns the function's value. A worker's error is raised here too.
- A pool reuses workers for many jobs. Creating a separate `threading.Thread` for each job gives you more direct control. Both use threads.
- In the saved practice, two 2-second fetches took 4.00 seconds in sequence and 2.02 seconds with two thread-pool workers. Three 2-second shops with two workers took 4.03 seconds. These are observed runs, not guaranteed timings.

---

## Python's Global Interpreter Lock (GIL)

The usual CPython build has a Global Interpreter Lock (GIL). In one interpreter with the GIL enabled, only one thread executes Python code at a time. The learner's Python 3.14 run reported `sys._is_gil_enabled()` as `True`.

- **I/O-bound work** spends time waiting for a network, disk or database. Threads can overlap those waits. The gain depends on the work and the external service.
- **CPU-bound Python work** spends time calculating. On a GIL-enabled build, adding threads usually does not let that Python code use several cores at once. In the saved short run, sequential work took 0.35 seconds and two threads took 0.34 seconds: effectively a tie, not proof of a speedup.
- Separate processes each have their own interpreter and GIL; see [Processes and CPU work](processes-and-gil.md). Optional free-threaded CPython builds can disable the GIL, so check the actual build instead of saying all Python threads behave identically.

The separate [async and await note](async-await.md) explains another way to overlap waiting. A blocking function such as `time.sleep()` inside `async def` still blocks its thread.

Sources: [Python threading](https://docs.python.org/3.14/library/threading.html), [Python executor pools](https://docs.python.org/3.14/library/concurrent.futures.html).

## What CPython means

Python is the language. CPython is the standard interpreter that runs it, mainly written in C. CPython is the interpreter's name; C is the language used to build it.

The GIL is managed automatically by the interpreter. You do not add it to your API code.

## Why two API results appear together

With `ThreadPoolExecutor(max_workers=2)`, up to two worker threads can be active. In GIL-enabled CPython, they take turns executing Python code, but their network waits overlap.

```text
Worker 1: send request -> wait ----------------> handle response
Worker 2:   send request -> wait ----------------> handle response
```

Both API servers can process requests simultaneously outside your interpreter. Python's response-handling turns can be close enough that both results appear together.

The GIL does not prevent both threads from being active or require the first API request to finish before the second starts. Blocking network operations normally release it while waiting.

## Why two Python calculations may not finish faster

With the same `max_workers=2`, suppose both workers run large arithmetic loops written in Python:

```text
Worker 1: calculate -> pause     -> calculate
Worker 2: pause     -> calculate -> pause
```

Both need Python execution time continuously. There is no long network wait to overlap. They share one Python execution slot under the GIL, so two workers usually do not halve the total time. Switching threads may add overhead.

Some libraries release the GIL while calculating in native code. This explanation applies to calculations written in Python, not every library operation.

Discussion saved on 29 October 2026. These explanations are not an independent assessment. [Separate recall questions](../../revision/concurrency-questions.md).

