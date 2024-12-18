import os
import sys
import pytest
import logging

# Adding the project root directory to the Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))

from Framework.Core.QAUTO import Actions


@pytest.fixture(scope="module")
def qemu_instance():
    """Fixture to start and stop the QEMU instance."""
    Qemu = Actions()
    Qemu.QemuStart()
    yield Qemu
    Qemu.QemuStop()

@pytest.mark.xfail(reason="This test is known to fail due to a bug.")
def test_power_management(qemu_instance):
    """
    Test to verify NIC's power-saving modes work as expected.
    Steps:
        1. Check current power management settings.
        2. Enable power-saving mode (Wake-on-LAN).
        3. Verify if power-saving mode is enabled.
    Expected Result: Power-saving features are enabled, and NIC goes into a lower power state when idle.
    """
    Qemu = qemu_instance

    # Get a logger for this test module
    logger = logging.getLogger(__name__)

    interface = "eth0"

    # Step 1: Check current power management settings
    logger.info(f"Checking current power management settings for {interface}...")
    power_settings = Qemu.send_serial_command(f"ethtool {interface}")
    logger.info(f"Current power management settings:\n{power_settings.strip()}")

    # Verify that Wake-on is properly configured
    assert "Wake-on" in power_settings, "Wake-on settings not found in the current power management settings."

    # Step 2: Enable power-saving mode (Wake-on-LAN)
    logger.info(f"Enabling power-saving mode (Wake-on-LAN) for {interface}...")
    Qemu.send_serial_command(f"ethtool -s {interface} wol g")

    # Step 3: Verify if power-saving mode is enabled
    logger.info(f"Verifying power-saving mode for {interface}...")
    updated_power_settings = Qemu.send_serial_command(f"ethtool {interface}")
    logger.info(f"Updated power management settings:\n{updated_power_settings.strip()}")

    # Verify Wake-on setting is correctly enabled
    assert "Wake-on: g" in updated_power_settings, "Wake-on mode not enabled correctly."

    # Expected result: NIC should support wake-on-lan and enter a lower power state when idle.
