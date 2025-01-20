import subprocess
import pytest
import re
from Inputs.common_inputs import Inputs

"This test case is to verify whether the interface can get an ip by using dhclient"

def get_current_ip():
    """Return the current IP address assigned to eth0, or None if no IP is assigned."""
    ip_result = subprocess.run(['ip', 'addr', 'show',Inputs.Interface], capture_output=True, text=True)
    for line in ip_result.stdout.splitlines():
        if "inet" in line:
            return line.split()[1]
    return None

def release_and_request_dhcp():
    """Release current IP and request a new IP via DHCP."""
    ip_address = get_current_ip()
    
    if ip_address:
        print(f"\nIP {ip_address} is currently assigned to eth0. Removing it.")
        subprocess.run(['sudo', 'ip', 'addr', 'del', ip_address, 'dev',Inputs.Interface])
    
    print("Requesting a new IP address via DHCP...")
    dhcp_result = subprocess.run(['sudo', 'dhclient', Inputs.Interface], capture_output=True, text=True)
    
    # Check if DHCP was successful
    if dhcp_result.returncode == 0:
        new_ip = get_current_ip()
        print(f"New IP address assigned: {new_ip}")
        return new_ip
    else:
        print(f"DHCP request failed with error: {dhcp_result.stderr}")
        return None

@pytest.fixture
def dhcp_assigned_ip():
    return release_and_request_dhcp()

def test_dhcp_assigned(dhcp_assigned_ip):
    """Test case to verify that the guest system receives an IP address from the DHCP server."""
    print(f"Assigned IP address after DHCP: {dhcp_assigned_ip}")
    
    assert dhcp_assigned_ip is not None, "No IP address assigned via DHCP"
    
    ip_pattern = re.compile(r'^\d+\.\d+\.\d+\.\d+/(\d+)$')
    assert ip_pattern.match(dhcp_assigned_ip), "Assigned IP is not in a valid format"
