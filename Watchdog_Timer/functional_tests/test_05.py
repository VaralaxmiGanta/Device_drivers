'''To verify if the watchdog timer can handle minimal timeout settings.
To know the minimal timeout value, run /sys/class/watchdog/watchdog0/min_timeout '''


from conftest import start_watchdog_service
import subprocess
import fileinput
import sys

def modify_watchdog_timeout(config_file_path="/etc/watchdog.conf", timeout=1):
    try:
        with fileinput.FileInput(config_file_path, inplace=True, backup='.bak') as file:
            for line in file:
                if line.strip().startswith("watchdog-timeout"):
                    print(f"watchdog-timeout = {timeout}")
                else:
                    print(line, end='')

        print(f"Watchdog timeout updated to {timeout} seconds in {config_file_path}")
    
    except Exception as e:
        print(f"Failed to modify the configuration file: {e}")

        
def test_automate_watchdog_timeout_change(timeout=1):
    config_file_path = "/etc/watchdog.conf"
    modify_watchdog_timeout(config_file_path=config_file_path, timeout=timeout)
    start_watchdog_service()

