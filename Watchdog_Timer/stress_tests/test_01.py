
import time
import pytest
import subprocess

@pytest.mark.parametrize('watchdog_device', ['/dev/watchdog'])
def test_continuous_watchdog_reset(watchdog_device):
    """Stress test to continuously reset the watchdog timer."""
    
    try:
        # Open the watchdog device for writing
        with open(watchdog_device, 'w') as f:
            start_time = time.time()
            # Write to the watchdog every 0.5 seconds for 1 minute
            for _ in range(120):
                f.write('1')  # Reset the watchdog timer
                f.flush()     # Make sure data is written immediately
                time.sleep(0.5)
            elapsed_time = time.time() - start_time
            assert elapsed_time < 70, "Watchdog timer failed to reset continuously within time."
            print("Continuous watchdog reset stress test passed.")
    except Exception as e:
        pytest.fail(f"Failed during continuous watchdog reset: {e}")
