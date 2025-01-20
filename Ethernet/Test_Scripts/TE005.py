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


def test_nic_speed(qemu_instance):
    """
    Test to verify NIC speed settings.
    Steps:
        1. Check the current speed using `ethtool eth0`.
        2. Set the speed to 1000Mb/s with full duplex using `ethtool -s eth0 speed 1000 duplex full`.
        3. Verify the speed matches the configuration using `ethtool eth0`.
    Expected Result: Speed updates successfully.
    """

    # Get a logger for this test module
    logger = logging.getLogger(__name__)

    Qemu = qemu_instance

    # Step 1: Check the current speed
    initial_speed = Qemu.send_serial_command("ethtool eth0 | grep 'Speed'")
    assert initial_speed, "Failed to get the current NIC speed."
    initial_speed_value = initial_speed.split(":")[1].strip()

    logger.info(f"Initial NIC Speed: {initial_speed_value}")

    # Step 2: Set the speed to 1000Mb/s with full duplex
    Qemu.send_serial_command("ethtool -s eth0 speed 1000 duplex full")

    # Step 3: Verify the new speed
    updated_speed = Qemu.send_serial_command("ethtool eth0 | grep 'Speed'")
    assert updated_speed, "Failed to get the updated NIC speed."
    updated_speed_value = updated_speed.split(":")[1].strip()

    logger.info(f"Updated NIC Speed: {updated_speed_value}")

    # Verify that the speed has been updated to 1000Mb/s
    assert "1000Mb/s" in updated_speed_value, f"Expected speed to be 1000Mb/s, but got {updated_speed_value}."
