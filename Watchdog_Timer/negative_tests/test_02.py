#Try to open the watchdog device when it’s already in use

import os
import pytest

WATCHDOG_DEVICE = "/dev/watchdog"

def test_device_busy():
    try:
        with open(WATCHDOG_DEVICE, 'w') as wd1:
            with pytest.raises(OSError):
                try:
                    with open(WATCHDOG_DEVICE, 'w') as wd2:
                        wd2.write('heartbeat')
                except OSError as e:
                    print(f"Caught expected OSError: {e}")
                    raise     
    except Exception as e:
        pytest.fail(f"Test failed with an unexpected exception: {e}")
