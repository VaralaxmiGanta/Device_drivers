''' checking the watchdog device at boundary of default watchdog timeout value.
Default value is 60s,here we have used 61s.
The system should reset as timeout value is excceded by 1sec'''

import os
import pytest
import time


WATCHDOG_DEVICE = "/dev/watchdog"

def test_keep_watchdog_active():
    try:
        with open(WATCHDOG_DEVICE, 'w') as wd:
            wd.write('heartbeat')
            time.sleep(61)  
            wd.write('heartbeat')
            wd.close()
            
    except PermissionError:
        pytest.skip("Insufficient permissions to access the watchdog device")
    except Exception as e:
        pytest.fail(f"Unexpected exception when keeping watchdog active: {e}")
