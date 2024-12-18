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


def test_nic_duplex_mode(qemu_instance):
    """
    Test to verify NIC duplex mode settings.
    Steps:
        1. Check the current duplex mode using `ethtool eth0`.
        2. Set the duplex mode to half using `ethtool -s eth0 duplex half`.
        3. Verify the duplex mode is set to half.
    Expected Result: Duplex setting changes as expected.
    """
    Qemu = qemu_instance

    # Get a logger for this test module
    logger = logging.getLogger(__name__)

    # Step 1: Check the current duplex mode
    initial_duplex = Qemu.send_serial_command("ethtool eth0 | grep 'Duplex'")
    assert initial_duplex, "Failed to get the current NIC duplex mode."
    initial_duplex_value = initial_duplex.split(":")[1].strip()

    logger.info(f"Initial NIC Duplex Mode: {initial_duplex_value}")

    # Step 2: Set the duplex mode to half
    Qemu.send_serial_command("ethtool -s eth0 duplex half")

    # Step 3: Verify the duplex mode has been set to half
    updated_duplex = Qemu.send_serial_command("ethtool eth0 | grep 'Duplex'")
    assert updated_duplex, "Failed to get the updated NIC duplex mode."
    updated_duplex_value = updated_duplex.split(":")[1].strip()

    logger.info(f"Updated NIC Duplex Mode: {updated_duplex_value}")

    # Verify that the duplex mode is set to half
    assert "Half" in updated_duplex_value, f"Expected duplex mode to be 'Half', but got {updated_duplex_value}."
