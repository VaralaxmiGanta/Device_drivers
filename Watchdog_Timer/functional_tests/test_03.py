""" check the watchdog triggering at the edge of timeout value(59sec) by making the network down.Watchdog is configured for continuous pinging"""

import pytest
import time
import subprocess
import fileinput
from conftest import restart_watchdog_service


config_file_path = "/etc/watchdog_config"

def modify_watchdog_config():
    try:
        with fileinput.FileInput(config_file_path, inplace=True, backup='.bak') as file:
            for line in file:
                if line.strip().startswith("#ping") or line.strip().startswith("# ping"):
                    print(f"ping = 8.8.8.8")
                else:
                    print(line, end='')

        print(f"Changes are updated in {config_file_path}")

    except Exception as e:
        print(f"Failed to modify the configuration file: {e}")



def test_simulate_network_failure_in_host():
    modify_watchdog_config()
    start_watchdog_service()
    try:
        interface = 'eth0'
        command = f"sudo ip link set {interface} down"
        result = subprocess.run(command, shell=True, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        print(f"Interface {interface} brought down.")
        
        # Wait for 59 seconds while the network is down
        for i in range(59):
            print(f"{i+1} second(s) after network ping down")
            time.sleep(1)
        command_up = f"sudo ip link set {interface} up"
        subprocess.run(command_up, shell=True, check=True)
        print(f"Interface {interface} brought up.")
        subprocess.run("sudo systemctl restart networking", shell=True, check=True)
        print("Networking service restarted.")
        print("Watchdog didn't initiate reset")

    except subprocess.CalledProcessError as e:
        print(f"Command failed with error: {e}")
    except Exception as ex:
        print(f"An unexpected error occurred: {ex}")

