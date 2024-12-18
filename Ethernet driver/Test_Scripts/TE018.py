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


def test_cable_functionality(qemu_instance):
    """
    Test the NIC’s functionality with a network cable.
    Steps:
        1. Plug the NIC into a Switch/Router.
        2. Check the NIC link status using ethtool.
        3. Verify connectivity by pinging the gateway or another host.
    Expected Result: The NIC should be able to connect through the network cable.
    """
    Qemu = qemu_instance

    # Get a logger for this test module
    logger = logging.getLogger(__name__)

    # Step 1: Plug the NIC into a Switch/Router (simulated by QEMU's virtual network)
    # Assuming the virtual NIC is already connected to a virtual switch or router.

    # Step 2: Check NIC Link Status
    logger.info("Checking NIC link status...")
    link_status = Qemu.send_serial_command("ethtool eth0")

    # Ensure the link is UP
    assert "Link detected: yes" in link_status, "Link is not up. Please check the connection."
    logger.info("NIC link is UP.")

    # Step 3: Test Connectivity by pinging the gateway or another host
    logger.info("Testing connectivity by pinging 192.168.122.1...")
    result = Qemu.send_serial_command("ping -c 4 192.168.122.1")

    # Verify the ping result
    assert "4 packets transmitted, 4 received" in result, "Ping failed. Connectivity issue with the network."
    logger.info("Ping successful. Connectivity is working.")

