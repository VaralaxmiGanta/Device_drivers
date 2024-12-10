import subprocess
import time


def reset_ethernet_interface(interface_name):
    print(f"Resetting interface {interface_name}...")
    subprocess.run(["sudo", "ip", "link", "set", interface_name, "down"], check=True)
    time.sleep(2)
    subprocess.run(["sudo", "ip", "link", "set", interface_name, "up"], check=True)
    print(f"Interface {interface_name} reset successfully.")


def check_interface_status(interface_name):
    print(f"Checking status of {interface_name}...")
    result = subprocess.run(["ip", "link", "show", interface_name], capture_output=True, text=True)
    if "state UP" in result.stdout:
        print(f"Interface {interface_name} is UP and running.")
        return True
    else:
        print(f"Interface {interface_name} is DOWN.")
        return False


def test_ping(target_ip="8.8.8.8"):
    print(f"Pinging {target_ip} to verify network connectivity...")
    result = subprocess.run(["ping", "-c", "4", target_ip], capture_output=True, text=True)
    if result.returncode == 0:
        print(f"Ping successful to {target_ip}.")
        return True
    else:
        print(f"Ping failed to {target_ip}.")
        return False


def full_test_case(interface_name="eth0"):
    reset_ethernet_interface(interface_name)
    if not check_interface_status(interface_name):
        print("Test Failed: Interface did not come up properly.")
        return
    if not test_ping():
        print("Test Failed: Unable to ping the network.")
        return

    print("Test Passed: Interface is UP and network is reachable.")


full_test_case("eth0")
