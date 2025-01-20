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


def test_loopback(qemu_instance):
    """
    Test the NIC’s internal loopback functionality.
    Steps:
        1. Enable loopback mode for the NIC (eth0).
        2. Ping the loopback address 127.0.0.1.
        3. Verify the response from the loopback.
    Expected Result: Loopback ping should be successful.
    """
    Qemu = qemu_instance

    # Get a logger for this test module
    logger = logging.getLogger(__name__)

    # Step 1: Enable loopback mode (bring the NIC up)
    logger.info("Enabling loopback mode on the NIC...")
    Qemu.send_serial_command("sudo ip link set eth0 up")

    # Step 2: Ping the loopback address (127.0.0.1)
    logger.info("Pinging the loopback address 127.0.0.1...")
    result = Qemu.send_serial_command("ping -c 4 127.0.0.1")

    # Step 3: Verify the response from the loopback
    assert "4 packets transmitted, 4 received" in result, "Loopback ping failed. No response from the NIC."
    logger.info("Loopback ping successful, received response from the NIC.")

