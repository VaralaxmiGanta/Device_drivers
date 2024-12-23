import subprocess
import pytest

"""This test case is to verify whether assigning of ip address to eth0 is successfull"""

# Function to configure network interface
def configure_interface(interface_name, ip_address, subnet_mask):
    try:
        print(f"Configuring {interface_name} with IP {ip_address}/{subnet_mask}...")
        # Assign IP address
        subprocess.run(
            ["sudo", "ip", "addr", "add", f"{ip_address}/{subnet_mask}", "dev", interface_name],
            check=True
        )
        print(f"Assigned IP {ip_address}/{subnet_mask} to {interface_name}")
        
        # Bring up the interface
        subprocess.run(["sudo", "ip", "link", "set", interface_name, "up"], check=True)
        print(f"Interface {interface_name} is now UP")
        return True
    except subprocess.CalledProcessError:
        print(f"Error configuring {interface_name}")
        return False

# Test case for successful configuration
@pytest.mark.parametrize(
    "interface_name, ip_address, subnet_mask",
    [("eth0", "192.168.1.100", "24")]
)
def test_network_configuration(interface_name, ip_address, subnet_mask):
    print(f"Starting configuration for {interface_name}...")
    result = configure_interface(interface_name, ip_address, subnet_mask)

    assert result is True, f"Failed to configure {interface_name} with IP {ip_address}/{subnet_mask}"
    print(f"{interface_name} successfully configured.")

    try:
        print(f"Verifying configuration for {interface_name}...")
        ip_result = subprocess.run(
            ["ip", "addr", "show", interface_name],
            capture_output=True, text=True, check=True
        )
        assert ip_address in ip_result.stdout, f"IP address {ip_address} not found on {interface_name}"
        print(f"IP address {ip_address} found on {interface_name}")

        link_result = subprocess.run(
            ["ip", "link", "show", interface_name],
            capture_output=True, text=True, check=True
        )
        assert "UP" in link_result.stdout, f"Interface {interface_name} is not UP"
        print(f"Interface {interface_name} is UP.")
        
    except subprocess.CalledProcessError as e:
        pytest.fail(f"Error in verifying network configuration: {e}")
