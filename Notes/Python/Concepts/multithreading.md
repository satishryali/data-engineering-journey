# Multithreading

Multithreading lets Python handle tasks that spend time waiting—such as downloading files, calling APIs, or querying a database—without freezing the entire program. While one thread waits for data, another thread can keep running.

---

## Why we need multithreading

In normal (synchronous) Python, code runs strictly line by line. If a database query or file download takes 3 seconds, Python stops and does nothing for 3 seconds.

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

### Output verified by running in notebook

```text
Before start: MainThread
Inside task: running on Thread-1 (slow_task)
After start: MainThread
Background work finished!
```

### How the important lines work:
- `target=slow_task`: Passes the function object itself without parentheses `()`.
- `t.start()`: Tells the operating system to start the new worker thread. It returns immediately in less than a millisecond, allowing `MainThread` to execute `After start` without waiting for the 3-second sleep.
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
Without `t.join()`, the main thread would try opening `amazon_v1.csv` while the background thread is still writing to it, causing empty reads or file lock conflicts.

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

Rather than taking 6 seconds (2s $\times$ 3), all three run together and complete in 2 seconds.

---

## Python's Global Interpreter Lock (GIL)

Python has a Global Interpreter Lock (GIL). Only one thread can execute Python bytecode at any single moment.
- **For I/O-bound tasks** (network requests, database queries, file writing): Threads spend most of their time waiting, so multithreading provides massive speedups.
- **For CPU-bound tasks** (heavy math, data compression, image processing): Threads do not run in parallel across multiple CPU cores. Use Python's `multiprocessing` module instead.

