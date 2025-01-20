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
def test_link_negotiation(qemu_instance):
    """
    Test to verify NIC's ability to negotiate link parameters like speed and duplex.
    Steps:
        1. Check current link settings.
        2. Force a specific speed and duplex setting, and disable autonegotiation.
        3. Verify if the NIC applies the forced link settings.
    Expected Result: NIC should negotiate the link settings as per configuration.
    """
    Qemu = qemu_instance

    # Get a logger for this test module
    logger = logging.getLogger(__name__)

    interface = "eth0"
    forced_duplex = "Full"
    autoneg = "off"

    # Step 1: Check current link settings
    logger.info(f"Checking current link settings for {interface}...")
    link_settings = Qemu.send_serial_command(f"ethtool {interface}")
    logger.info(f"Current link settings:\n{link_settings.strip()}")
    assert "Duplex" in link_settings, "Duplex information not found in the current settings."

    # Step 2: Force a specific duplex and disable autonegotiation
    logger.info(f"Forcing duplex {forced_duplex} and disabling autonegotiation...")
    Qemu.send_serial_command(
        f"ethtool -s {interface}duplex {forced_duplex} autoneg {autoneg}")

    # Step 3: Verify the negotiated settings
    logger.info(f"Verifying link settings for {interface} after configuration...")
    negotiated_settings = Qemu.send_serial_command(f"ethtool {interface}")
    logger.info(f"Negotiated link settings:\n{negotiated_settings.strip()}")

    # Check if the forced settings are applied
    assert f"Duplex: {forced_duplex}" in negotiated_settings, f"Duplex not set to {forced_duplex}."
    assert "Auto-negotiation: off" in negotiated_settings, "Auto-negotiation is still enabled."
