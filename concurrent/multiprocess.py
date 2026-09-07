import time
import multiprocessing
from concurrent.futures import ProcessPoolExecutor

ids = range(10)

def worker(id, shared_dict, lock):
    local_counter = 0

    for _ in range(100000):
        local_counter += 1

    with lock:
        shared_dict["counter"] += local_counter
        return shared_dict["counter"]

if __name__ == "__main__":
    with multiprocessing.Manager() as manager:
        shared_dict = manager.dict({ "counter": 0 })
        lock = manager.Lock()

        with ProcessPoolExecutor() as executor:
            results = executor.map(worker, ids, [shared_dict]*10, [lock]*10)
            for msg in results:
                print(msg)
