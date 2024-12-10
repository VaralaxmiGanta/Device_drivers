import subprocess
import pytest

# Define a fixture for the interface
@pytest.fixture
def interface():
    return "eth0"

@pytest.fixture
def mtu_size():
    return 5000

def set_mtu(interface, mtu_size):
    try:
        command = f"sudo ip link set {interface} mtu {mtu_size}"
        subprocess.run(command, shell=True, check=True)
        print(f"MTU for {interface} set to {mtu_size}")
    except subprocess.CalledProcessError as e:
        print(f"Failed to set MTU for {interface}. Error: {e.stderr.strip()}")

def get_mtu(interface):
    try:
        command = f"ip link show {interface} | grep -oP 'mtu \K\d+'"
        result = subprocess.run(command, shell=True, text=True, capture_output=True, check=True)
        return result.stdout.strip()
    except subprocess.CalledProcessError as e:
        print(f"Failed to get MTU for {interface}. Error: {e.stderr.strip()}")
        return None

def print_ip_link(interface):
    try:
        command = f"ip link show {interface}"
        result = subprocess.run(command, shell=True, text=True, capture_output=True, check=True)
        print(result.stdout.strip())
    except subprocess.CalledProcessError as e:
        print(f"Failed to get interface details for {interface}. Error: {e.stderr.strip()}")

def test_mtu(interface, mtu_size):
    set_mtu(interface, mtu_size)
    print_ip_link(interface)
    mtu = get_mtu(interface)
    if mtu and f"{mtu_size}" in mtu:
        print(f"MTU for {interface} is correctly set to {mtu_size}")
    else:
        print(f"MTU for {interface} is not correctly set to {mtu_size}. Got: {mtu}")

if __name__ == "__main__":
    pytest.main()
