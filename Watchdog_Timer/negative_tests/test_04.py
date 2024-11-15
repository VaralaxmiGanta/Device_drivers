"""
Test writing to the watchdog when it is disabled.
Disable the watchdog device manually for the test (simulating a disabled device).
It will give Device not found
"""
import pytest
import os

WATCHDOG_DEVICE_PATH = "/dev/watchdog"

def test_write_to_disabled_watchdog():
    try:
        if not os.path.exists(WATCHDOG_DEVICE_PATH):
            raise FileNotFoundError(f"Watchdog device not found at {WATCHDOG_DEVICE_PATH}")
        with pytest.raises(OSError):
            with open(WATCHDOG_DEVICE_PATH, 'w') as wd:
                wd.write("test")      
    except FileNotFoundError as fnf_error:
        pytest.fail(f"Watchdog device not found: {fnf_error}")
    except OSError as os_error:
        pytest.fail(f"Error while writing to the disabled watchdog: {os_error}")
    except Exception as e:
        pytest.fail(f"An unexpected error occurred: {e}")
