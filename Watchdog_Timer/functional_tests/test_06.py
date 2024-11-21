'''To verify if the watchdog timer can handle maximum timeout settings.
To know the maximum timeout value, run /sys/class/watchdog/watchdog0/max_timeout '''


from conftest inport start_watchdog_service
import subprocess
import fileinput
import sys

def modify_watchdog_timeout(config_file_path="/etc/watchdog.conf", timeout=65535):
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

        
def test_automate_watchdog_timeout_change(timeout=65535):
    config_file_path = "/etc/watchdog.conf"
    modify_watchdog_timeout(config_file_path=config_file_path, timeout=timeout)
    start_watchdog_service()

