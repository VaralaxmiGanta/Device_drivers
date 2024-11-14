
''' write "heartbeat" to the watchdog device and don't close the file which results in resetting the system after the default timeout expired'''
import os
import pytest
import time


WATCHDOG_DEVICE = "/dev/watchdog"

def test_keep_watchdog_active():
    try:
        with open(WATCHDOG_DEVICE, 'w') as wd:
            wd.write('heartbeat')
    except PermissionError:
        pytest.skip("Insufficient permissions to access the watchdog device")
    except Exception as e:
        pytest.fail(f"Unexpected exception when keeping watchdog active: {e}")
