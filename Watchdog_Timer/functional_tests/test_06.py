'''To verify if the watchdog timer can handle maximum timeout settings.
To know the maximum timeout value, run /sys/class/watchdog/watchdog0/max_timeout '''


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

def restart_watchdog_service():
    try:
        subprocess.run(["sudo", "systemctl", "stop", "watchdog"], check=True)        
        subprocess.run(["sudo", "systemctl", "start", "watchdog"], check=True)
        print("Watchdog service restarted successfully.")
    
    except subprocess.CalledProcessError as e:
        print(f"Failed to restart the watchdog service: {e}")
        
def test_automate_watchdog_timeout_change(timeout=65535):
    config_file_path = "/etc/watchdog.conf"
    
    # Step 1: Modify the watchdog timeout in the config file
    modify_watchdog_timeout(config_file_path=config_file_path, timeout=timeout)
    
    # Step 2: Restart the watchdog service to apply the changes
    restart_watchdog_service()

