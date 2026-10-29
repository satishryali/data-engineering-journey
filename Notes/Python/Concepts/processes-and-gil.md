# Processes and the virtual environment

Use separate processes when large calculations written in Python need more than one CPU core. A process is a separate running program with its own memory.

## Threads and processes

With CPython's GIL enabled:

| Pool with `max_workers=2` | Workers | Python calculations |
| --- | --- | --- |
| `ThreadPoolExecutor` | Two threads sharing a process and its memory | Take turns under that interpreter's GIL |
| `ProcessPoolExecutor` | Two processes with separate interpreters and GILs | Can execute on different CPU cores simultaneously |

The main process also exists and collects results. Available cores, startup and moving data between processes affect speed. Small calculations can be slower with a process pool.

## Which Python and .venv do workers use?

They are separate running instances, usually of the same Python executable. They are not separate Python installations.

If the main script runs with your `.venv` Python, spawned workers normally use that executable too. They can use the packages installed there. You do not need another `.venv` for each worker.

```text
.venv Python executable
  main process       -> its own interpreter and memory
  worker process 1   -> its own interpreter and memory
  worker process 2   -> its own interpreter and memory
```

The installed environment is shared on disk. Ordinary Python variables are not automatically shared between processes. Custom configuration can change the worker executable.

## Small calculation example

Goal: calculate squares for two order quantities. Input: `[4, 7]`.

Save this as a standalone `.py` file and run it using the desired environment's Python. A notebook-defined worker may not be importable by process workers.

```python
from concurrent.futures import ProcessPoolExecutor

def square_quantity(quantity):
    return quantity * quantity

if __name__ == "__main__":
    with ProcessPoolExecutor(max_workers=2) as executor:
        results = list(executor.map(square_quantity, [4, 7]))
    print(results)
```

Expected output:

```text
[16, 49]
```

- Define the worker at the top level so workers can import it.
- The main guard keeps imported code from creating another pool on Windows.
- `map()` returns results in input order.
- This tiny example shows usage, not a speed benefit or proof that both workers handled an input.

## Why the first Windows run failed

The learner's first process script put its comparison code outside the main guard. On Windows, a worker starts a fresh interpreter and reads the script to find the worker function. It also ran the top-level sequential and thread comparisons, then tried to start another process pool while it was still starting. Python raised `RuntimeError`; the main process later saw `BrokenProcessPool` at `future.result()`.

Put only function definitions and safe imports above `if __name__ == "__main__":`. Put the code that starts the pool inside it. When the script is run directly, its `__name__` is `"__main__"`. A spawned worker reads it under a different name (in this run, `"__mp_main__"`), so the worker finds the function but skips the pool-starting block.

The short saved CPU comparison showed 0.35 seconds sequential and 0.34 seconds with threads: effectively a tie. The learner later reported 0.28 seconds for a process-pool run; that is 0.06 seconds less than 0.34, not 0.6. One short run does not prove that processes are always faster. The process timer in the current script includes pool startup and shutdown.

## Sources and learning context

Explained on 29 October 2026. A separate virtual-environment discussion supplied no worker executable path. The learner also supplied an earlier process-startup traceback and reported a later 0.28-second process result; the full corrected terminal output was not saved in this chat. Tutor help was used for the guard diagnosis. Existing `practice/Sync/Async/mulitprocess.py` was inspected, not changed by the tutor. No independent assessment is recorded.

- [Multiprocessing and spawned interpreters](https://docs.python.org/3.14/library/multiprocessing.html#contexts-and-start-methods)
- [Default worker executable](https://docs.python.org/3.14/library/multiprocessing.html#multiprocessing.set_executable)
- [ProcessPoolExecutor](https://docs.python.org/3.14/library/concurrent.futures.html#processpoolexecutor)
- [Threads and the GIL](multithreading.md)
- [Recall questions](../../revision/concurrency-questions.md)
