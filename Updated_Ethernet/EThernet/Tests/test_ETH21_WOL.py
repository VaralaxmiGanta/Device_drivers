import subprocess
import pytest
from Inputs.common_inputs import Inputs

"""THis test case is to verifyy whether the wol is enabled for the interface """

def get_wol_status(interface):
    """Retrieve the Wake-on-LAN status of the network interface."""
    result = subprocess.run(
        ["ethtool", interface],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
    )
    if result.returncode != 0:
        return None
    for line in result.stdout.splitlines():
        if line.strip().startswith("Wake-on"):
            return line.split(":")[1].strip()
    return None

@pytest.fixture
def setup_network_interface():
    """Fixture to provide the network interface for testing."""
    return Inputs.Interface

def test_verify_wol_enabled(setup_network_interface):
    """Test to verify that WoL is enabled on the network interface."""
    interface = setup_network_interface

    # Step 1: Check the WoL status
    wol_status = get_wol_status(interface)
    print(f"Wake-on-LAN status for {interface}: {wol_status}")
    assert wol_status is not None, f"Could not retrieve WoL status for {interface}."
    
    # Step 2: Assert that WoL is enabled (status should be 'g')
    assert wol_status == "g", f"Wake-on-LAN is not enabled for {interface} (status: {wol_status})."

    # Step 3 (Optional): Enable WoL if disabled
    if wol_status != "g":
        print(f"Enabling WoL on {interface}.")
        subprocess.run(["sudo", "ethtool", "-s", interface, "wol", "g"], check=True)
        wol_status = get_wol_status(interface)
        assert wol_status == "g", f"Failed to enable Wake-on-LAN for {interface}."

