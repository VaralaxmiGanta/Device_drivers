"""Fixture to enable the watchdog device and set its timeout before each test."""


import subprocess
import pytest
import fileinput

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

def stop_watchdog_service():
    try:
        subprocess.run(["sudo", "systemctl", "stop", "watchdog"], check=True)
        print("Watchdog service stopped successfully.")
    except subprocess.CalledProcessError as e:
        pytest.fail(f"Failed to stop the watchdog service: {e}")

def unload_watchdog_module():
    try:
        subprocess.run(['sudo','modprobe', '-r', 'softdog'], check=True)
        print("Watchdog device unloaded.")
    except subprocess.CalledProcessError as e:
        pytest.fail(f"Failed to unload the watchdog device: {e}")

@pytest.fixture(scope="function", autouse=True)
def manage_watchdog_device():
    load_watchdog_device()

    modify_watchdog_config()

    start_watchdog_service()
    
    stop_watchdog_service()
  
    yield

    unload_watchdog_module()
