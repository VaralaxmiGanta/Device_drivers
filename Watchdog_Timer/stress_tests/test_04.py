"""
    Stress test for writing heartbeat signals in parallel from multipl
e threads.
    This should simulate concurrent access to the watchdog and test th
read-safety.
 """
    
import pytest
import os
import time
import threading

WATCHDOG_DEVICE_PATH = "/dev/watchdog"

@pytest.fixture
def setup_watchdog():
    if not os.path.exists(WATCHDOG_DEVICE_PATH):
        pytest.skip("Watchdog device not available")
    yield

def test_parallel_heartbeat_writes(setup_watchdog):
    def write_heartbeat():
        with open(WATCHDOG_DEVICE_PATH, 'w') as wd:
            for _ in range(10000):  
                wd.write("heartbeat")

    threads = []
    start_time = time.time()
    for _ in range(10):  
        t = threading.Thread(target=write_heartbeat)
        threads.append(t)
        t.start()

    for t in threads:
        t.join()

    elapsed_time = time.time() - start_time
    print(f"Parallel write stress test took {elapsed_time:.2f} seconds
")
    assert elapsed_time < 30  
