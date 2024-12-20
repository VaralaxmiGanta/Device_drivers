
''' write "heartbeat" to the watchdog device which results in resetting the system after the default timeout expired'''
import os
import pytest
import time


WATCHDOG_DEVICE = "/dev/watchdog"

def test_keep_watchdog_active():
    try:
        with open(WATCHDOG_DEVICE, 'w') as wd:
            wd.write('heartbeat')
        print("now watchdog will reboot the system in 60 seconds")
    except PermissionError:
        pytest.skip("Insufficient permissions to access the watchdog device")
    except Exception as e:
        pytest.fail(f"Unexpected exception when keeping watchdog active: {e}")
