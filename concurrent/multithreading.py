import time
from concurrent.futures import ThreadPoolExecutor
from threading import Lock

counter_lock = Lock()
counter = 0
ids = range(10)

def worker(id):
    global counter_lock, counter
    time.sleep(1)
    with counter_lock:
        for _ in range(100000):
            counter += 1

    return counter

with ThreadPoolExecutor() as executor:
    results = executor.map(worker, ids)
    for msg in results:
        print(msg)
