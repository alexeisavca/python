import time
import pytest
from retrier import retryable, MaxRetriesException
from random import randint
from unittest.mock import Mock 
from random import randint

mock_sleep = Mock()

def test_max_retries(monkeypatch):
    monkeypatch.setattr(time, "sleep", mock_sleep)
    retries = randint(0, 100)
    timeout = randint(0, 100)
    logger = Mock()
    exception = Exception("boom!")
    def func():
        raise exception

    with pytest.raises(MaxRetriesException, match=f"Failed after {retries} retries"):
        retryable(retries=retries, timeout=timeout, logger=logger)(func)()

    mock_sleep.assert_called_with(timeout)
    logger.assert_called_with(exception)
    
    assert mock_sleep.call_count == retries
    assert logger.call_count == retries


def test_happy_path():
    arg1 = randint(0, 100)
    arg2 = randint(0, 100)

    def func(a, b=-1):
        return f"{a} {b}"

    assert retryable()(func)(arg1, b=arg2) == f"{arg1} {arg2}"