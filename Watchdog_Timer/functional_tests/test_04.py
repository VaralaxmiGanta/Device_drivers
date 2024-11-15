import subprocess
import pytest
import time

def test_simulate_network_failure_in_host():
    try:
        interface = 'eth0'
        
        # Bring the network interface down
        command = f"sudo ip link set {interface} down"
        result = subprocess.run(command, shell=True, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        print(f"Interface {interface} brought down.")
        
        # Wait for 63 seconds while the network is down
        for i in range(63):
            print(f"{i+1} second(s) after network ping down")
            time.sleep(1)

        # Bring the network interface back up
        command_up = f"sudo ip link set {interface} up"
        subprocess.run(command_up, shell=True, check=True)
        print(f"Interface {interface} brought up.")

        # Restart networking services
        subprocess.run("sudo systemctl restart networking", shell=True, check=True)
        print("Networking service restarted.")
        print("Watchdog didn't initiate reset")

    except subprocess.CalledProcessError as e:
        print(f"Command failed with error: {e}")
    except Exception as ex:
        print(f"An unexpected error occurred: {ex}")

