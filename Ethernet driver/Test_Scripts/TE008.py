import os
import sys
import pytest
import logging

# Add the project root directory to the Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))

from Framework.Core.QemuAutomation import Actions

@pytest.fixture(scope="module")
def qemu_instance():
    """Fixture to start and stop the QEMU instance."""
    Qemu = Actions()
    Qemu.QemuStart()
    yield Qemu
    Qemu.QemuStop()

def test_mac_address_change(qemu_instance):
    """
    Test to verify NIC's MAC address can be changed.
    Steps:
        1. Check the current MAC address using `ip link show eth0`.
        2. Change the MAC address using `sudo ip link set dev eth0 address 02:42:ac:11:00:02`.
        3. Verify the MAC address change using `ip link show eth0`.
    Expected Result: MAC address is updated successfully.
    """
    Qemu = qemu_instance

    # Get a logger for this test module
    logger = logging.getLogger(__name__)

    # Step 1: Check current MAC address
    current_mac_address = Qemu.send_serial_command("ip link show eth0 | grep 'link/ether'")
    logger.info(f"Current MAC Address: {current_mac_address.strip()}")

    # Step 2: Change the MAC address
    Qemu.send_serial_command("ip link set dev eth0 address 02:42:ac:11:00:02")

    # Step 3: Verify the MAC address change
    new_mac_address = Qemu.send_serial_command("ip link show eth0 | grep 'link/ether'")
    logger.info(f"New MAC Address: {new_mac_address.strip()}")

    # Assert the new MAC address is correctly updated
    assert "02:42:ac:11:00:02" in new_mac_address, f"Expected MAC address '02:42:ac:11:00:02', but got {new_mac_address.strip()}"
