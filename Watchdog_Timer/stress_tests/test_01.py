"""
    Stress test for writing a heartbeat to the watchdog continuously without pause.
    This should push the system to handle rapid, continuous writes.
"""    
import pytest
import os
import time

WATCHDOG_DEVICE_PATH = "/dev/watchdog"

@pytest.fixture
def setup_watchdog():
    if not os.path.exists(WATCHDOG_DEVICE_PATH):
        pytest.skip("Watchdog device not available")
    yield


def test_continuous_heartbeat_write(setup_watchdog):
    try:
        with open(WATCHDOG_DEVICE_PATH, 'w') as wd:
            start_time = time.time()

            for _ in range(100000): 
                try:
                    wd.write("heartbeat")
                except IOError as e:
                    pytest.fail(f"Failed to write to watchdog device: {e}")
                    return             
            elapsed_time = time.time() - start_time
            print(f"Continuous write stress test took {elapsed_time:.2f} seconds")
            
            assert elapsed_time < 210, f"Test took too long: {elapsed_time:.2f} seconds"
    
    except Exception as e:
        pytest.fail(f"An unexpected error occurred during the test: {e}")

