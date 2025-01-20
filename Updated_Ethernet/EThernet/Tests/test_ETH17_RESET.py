import subprocess
import time
import pytest
from Inputs.common_inputs import Inputs

"""THis test case is to verify whether the interface can reinitialize the link and all after resetting the interface"""

@pytest.fixture
def reset_ethernet_interface():
    """Fixture to reset Ethernet interface."""
    interface_name = Inputs.Interface
    print(f"Resetting interface {interface_name}...\n")
    subprocess.run(["sudo", "ip", "link", "set", interface_name, "down"], check=True)
    time.sleep(2)
    subprocess.run(["sudo", "ip", "link", "set", interface_name, "up"], check=True)
    print(f"Interface {interface_name} reset successfully.\n")
    
    # Ensure the default gateway is restored
    default_gateway = "10.0.2.2"
    print(f"Restoring default gateway via {default_gateway}...\n")
    subprocess.run(["sudo", "ip", "route", "add", "default", "via", default_gateway], check=True)
    print("Default gateway restored.\n")
    
    yield interface_name  # Return the interface name for further tests


@pytest.fixture
def check_interface_status(reset_ethernet_interface):
    """Fixture to check the interface status."""
    interface_name = reset_ethernet_interface
    print(f"Checking status of {interface_name}...")
    result = subprocess.run(["ip", "link", "show", interface_name], capture_output=True, text=True)
    if "state UP" in result.stdout:
        print(f"Interface {interface_name} is UP and running.\n")
        return True
    else:
        print(f"Interface {interface_name} is DOWN.")
        return False


@pytest.fixture
def test_ping():
    """Fixture to ping a target IP address."""
    target_ip = "8.8.8.8"
    print(f"Pinging {target_ip} to verify network connectivity...\n")
    result = subprocess.run(["sudo", "ping", "-c", "4", target_ip], capture_output=True, text=True)
    if result.returncode == 0:
        print(f"Ping successful to {target_ip}.")
        return True
    else:
        print(f"Ping failed to {target_ip}.")
        return False


def test_full_network_test(reset_ethernet_interface, check_interface_status, test_ping):
    """Test case combining the Ethernet reset, interface status check, and ping test."""
    assert check_interface_status, "Test Failed: Interface did not come up properly."
    assert test_ping, "Test Failed: Unable to ping the network."

    print("Test Passed: Interface is UP and network is reachable.")
