
''' writing invalid data to  the watchdog timer should not trigger the reset.The valid data is "heartbeat" or any numeric value'''

import os
import pytest
import time


WATCHDOG_DEVICE = "/dev/watchdog"

def test_invalid_write():
    try:
        with open(WATCHDOG_DEVICE, 'w') as wd:
            wd.write('invalid_data')
            time.sleep(1)
            assert not wd.closed, "Watchdog device should still be open after invalid data write"
    except Exception as e:
        print(f"Unexpected error occurred during invalid write test: {e}")
        pytest.fail(f"Test failed due to an unexpected exception: {e}")
