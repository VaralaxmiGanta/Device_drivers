import os
import sys
import pytest
import logging

# Add the project root directory to the Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))

from Framework.Core.QAUTO import Actions

@pytest.fixture(scope="module")
def qemu_instance():
    """Fixture to start and stop the QEMU instance."""
    Qemu = Actions()
    Qemu.QemuStart()
    yield Qemu
    Qemu.QemuStop()

def test_nic_auto_negotiation(qemu_instance):
    """
    Test to verify NIC auto-negotiation for speed and duplex.
    Steps:
        1. Enable auto-negotiation using `ethtool -s eth0 autoneg on`.
        2. Check the NIC settings to confirm auto-negotiation is enabled.
    Expected Result: NIC negotiates speed/duplex with the connected device.
    """
    Qemu = qemu_instance

    # Get a logger for this test module
    logger = logging.getLogger(__name__)

    # Step 1: Enable auto-negotiation
    Qemu.send_serial_command("ethtool -s eth0 autoneg on")

    # Step 2: Check current NIC settings to confirm auto-negotiation is enabled
    auto_negotiation_status = Qemu.send_serial_command("ethtool eth0 | grep 'Auto-negotiation'")

    assert auto_negotiation_status, "Failed to get the NIC auto-negotiation status."
    auto_negotiation_value = auto_negotiation_status.split(":")[1].strip()

    logger.info(f"Auto-negotiation status: {auto_negotiation_value}")

    # Verify that auto-negotiation is enabled
    assert "on" in auto_negotiation_value, f"Expected auto-negotiation to be 'on', but got {auto_negotiation_value}."
