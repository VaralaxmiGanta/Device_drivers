"""Test accessing watchdog without sufficient permissions.
    Accessing the watchdog as a non-root user should raise a PermissionError.
    run this test case with --noconftest option while using pytest and don't use sudo to get the accurate output
"""
import subprocess
import pytest
import fileinput
import os

config_file_path="/etc/watchdog.conf"

def load_watchdog_module():
    try:
        subprocess.run(['sudo','modprobe', 'softdog'], check=True)
        print("Watchdog module loaded.")
    except subprocess.CalledProcessError as e:
        pytest.fail(f"Failed to load the watchdog device or set the timeout: {e}")


def modify_watchdog_config():
    try:
        with fileinput.FileInput(config_file_path, inplace=True, backup='.bak') as file:
            for line in file:
                if line.strip().startswith("#watchdog-device") or line.strip().startswith("# watchdog-device"):
                    print("watchdog-device = /dev/watchdog")
                elif line.strip().startswith("#watchdog-timeout") or line.strip().startswith("# watchdog-timeout"):
                    print("watchdog-timeout = 60")
                else:
                    print(line, end='')

        print(f"watchdog device is enabled and timeout is set to default in {config_file_path}")

    except Exception as e:
        print(f"Failed to modify the configuration file: {e}")


def start_watchdog_service():
    try: 
        subprocess.run(["sudo", "systemctl", "start", "watchdog"], check=True)
        print("Watchdog service started successfully.")

    except subprocess.CalledProcessError as e:
        print(f"Failed to restart the watchdog service: {e}")


@pytest.mark.no_fixture
def test_access_without_permissions():
    load_watchdog_module()
    modify_watchdog_config()
    start_watchdog_service()
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
        
    except Exception as e:
        print(f"Unexpected error occurred: {e}")
        pytest.fail(f"An unexpected error occurred: {e}")
