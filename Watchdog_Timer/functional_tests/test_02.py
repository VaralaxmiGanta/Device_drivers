'''check whether the watchdog initiates reboot when there is no network activity done while the interface is enabled.'''

from confest import restart_watchdog_service
import subprocess
import time
import re
import fileinput


config_file_path="/etc/watchdog.conf"

def modify_watchdog_config():
    try:
        with fileinput.FileInput(config_file_path, inplace=True, backup='.bak') as file:
            for line in file:
                if line.strip().startswith("#interface") or line.strip().startswith("# interface"):
                    print(f"interface = eth0")
                else:
                    print(line, end='')

        print(f"Changes are updated in {config_file_path}")

    except Exception as e:
        print(f"Failed to modify the configuration file: {e}")



def test_simulate_network_failure_in_host():
    modify_watchdog_config()
    start_watchdog_service()
    print("watchdog will initiate reboot in 60 sec as there is no continuous network activity is occuring") 
    
    


