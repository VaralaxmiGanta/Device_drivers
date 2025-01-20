import subprocess
import pytest

"""This test case is to verify that driver responds correctly when requesting data of invalid interface"""

def check_network_interface(interface):
    try:
        result = subprocess.run(
            ["ip", "link", "show", interface],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            check=True,
        )
        return result.stdout
    except subprocess.CalledProcessError:
        return None

@pytest.fixture
def setup_invalid_interface():
    """Fixture to simulate using a non-existent network interface"""
    return "non_existent_interface"

def test_invalid_network_interface(setup_invalid_interface):
    """Test the behavior when an invalid or non-existent network interface is specified"""
    interface = setup_invalid_interface
    
    # Step 1: Attempt to check the status of the invalid network interface
    interface_status = check_network_interface(interface)
    
    # Step 2: Assert that the interface does not exist
    assert interface_status is None, f"Expected no output for invalid interface {interface}, but got {interface_status}"

    result = subprocess.run(
        ["ip", "link", "set", interface, "up"],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
    )
    
    assert result.returncode != 0, f"Expected error when bringing up non-existent interface {interface}, but got no error."

    print(result.stderr)
