""" check the watchdog triggering at one second beyond the timeout value(61sec) by making the network down.Watchdog is configured for continuous pinging"""


import subprocess
import pytest
import time
import subprocess
import fileinput
from conftest import start_watchdog_service
from conftest import stop_watchdog_service


config_file_path = '/etc/watchdog.conf'

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
    stop_watchdog_service()
    start_watchdog_service()
    try:
        interface = 'eth0'
        command = f"sudo ip link set {interface} down"
        result = subprocess.run(command, shell=True, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        print(f"Interface {interface} brought down.")
        for i in range(61):
            print(f"{i+1} second(s) after network ping down")
            time.sleep(1)

        '''command_up = f"sudo ip link set {interface} up"
        subprocess.run(command_up, shell=True, check=True)
        print(f"Interface {interface} brought up.")

        # Restart networking services
        subprocess.run("sudo systemctl restart networking", shell=True, check=True)
        print("Networking service restarted.")'''

        print("Now watchdog  timer will initiate reset")
    except subprocess.CalledProcessError as e:
        print(f"Command failed with error: {e}")
    except Exception as ex:
        print(f"An unexpected error occurred: {ex}")
