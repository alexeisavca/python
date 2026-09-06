import time
from functools import wraps

class MaxRetriesException(Exception):
    pass

def retryable(retries=3, timeout=0.002, logger=lambda: None):
    def decorator(cb):
        @wraps(cb)
        def wrapper(*args, **kwargs):
            print(logger)
            for _ in range(retries):
                try:
                    return cb(*args, **kwargs)
                except Exception as e:
                    logger(e)
                    time.sleep(timeout)

            raise MaxRetriesException(f"Failed after {retries} retries")

        return wrapper

    return decorator