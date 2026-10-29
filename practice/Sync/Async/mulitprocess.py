import os
from concurrent.futures import ProcessPoolExecutor
from concurrent.futures import ThreadPoolExecutor
import time

def calculate(limit):
    total = 0
    for i in range(limit):
        total += i * i
    return total,os.getpid(),__name__
if __name__ == "__main__":
    limit = 5_000_000
    #sequential timer 
    seq_start = time.perf_counter()
    first_job = calculate(limit)
    second_job = calculate(limit)
    print("first job : ",first_job)
    print("second job : ",second_job)
    print("Sequential Timer : ",round(time.perf_counter()  - seq_start,2))

    #threadpoolexecutor
    thread_time = time.perf_counter()
    with ThreadPoolExecutor(max_workers=2) as executor:
        thread1 = executor.submit(calculate,limit)
        thread2 = executor.submit(calculate,limit)
        print("Thread 1 result : ", thread1.result())
        print("Thread 2 result : ", thread2.result())

    print("Thread timer : ",round(time.perf_counter() - thread_time,2))

    #Process pool executor 
    mulprocess_start = time.perf_counter()
    with ProcessPoolExecutor(max_workers=2) as executor:
        first_process = executor.submit(calculate,limit)
        second_process = executor.submit(calculate,limit)
        print(first_process.result())
        print(second_process.result())
    print("process timer : ",round(time.perf_counter() - mulprocess_start,2))