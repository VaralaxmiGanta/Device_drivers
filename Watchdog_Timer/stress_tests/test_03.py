 """
    Stress test for writing a heartbeat to the watchdog with very short sleep intervals.
    This should simulate high-frequency writes to check the watchdog's ability to handle them.
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

def test_continuous_heartbeat_with_short_interval(setup_watchdog):
   with open(WATCHDOG_DEVICE_PATH, 'w') as wd:
        start_time = time.time()
        for _ in range(100000):  
            wd.write("heartbeat")
            time.sleep(0.001)  
        elapsed_time = time.time() - start_time
        print(f"High-frequency write stress test took {elapsed_time:.2f} seconds")
        assert elapsed_time < 210

