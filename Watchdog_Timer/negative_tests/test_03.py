"""Test accessing watchdog without sufficient permissions.
    Accessing the watchdog as a non-root user should raise a PermissionError.
"""
    
import pytest
import os

WATCHDOG_DEVICE_PATH = "/dev/watchdog"

def test_access_without_permissions():
    try:
        if not os.path.exists(WATCHDOG_DEVICE_PATH):
            raise FileNotFoundError(f"Watchdog device not found at {WATCHDOG_DEVICE_PATH}")

        with pytest.raises(PermissionError):
            with open(WATCHDOG_DEVICE_PATH, 'w') as wd:
                wd.write("test")  

    except FileNotFoundError as fnf_error:
        print(f"File not found error: {fnf_error}")
        pytest.fail(f"Watchdog device not found: {fnf_error}")  
    except PermissionError as perm_error:
        print(f"Permission error: {perm_error}")
        pytest.fail(f"Permission error while accessing {WATCHDOG_DEVICE_PATH}: {perm_error}")
    except Exception as e:
        print(f"Unexpected error occurred: {e}")
        pytest.fail(f"An unexpected error occurred: {e}")
