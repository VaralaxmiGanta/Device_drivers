import os
import sys
import pytest
import time
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

@pytest.mark.skip(reason="This test cant be executed because it closes the connection with the Qemu system while execution.")
def test_fault_tolerance(qemu_instance):
    """
    Test the NIC's ability to recover from faults.
    Steps:
        1. Disconnect the NIC physically (simulated in QEMU).
        2. Reboot the system using QemuRestart.
        3. Reconnect the NIC.
        4. Verify NIC availability after reboot.
    Expected Result: NIC should re-initialize correctly after reboot and reconnect.
    """
    Qemu = qemu_instance

    # Get a logger for this test module
    logger = logging.getLogger(__name__)

    # Step 1: Simulate disconnecting the NIC
    logger.info("Simulating NIC disconnection...")
    Qemu.send_serial_command("ip link set eth0 down")

    # Step 2: Reboot the system
    logger.info("Rebooting the system...")
    Qemu.QemuRestart()  # This function reboots the QEMU instance

    # Step 3: Reconnect the NIC
    time.sleep(5)  # Wait for the system to reboot
    logger.info("Reconnecting the NIC...")
    Qemu.send_serial_command("ip link set eth0 up")

    # Step 4: Verify NIC availability
    logger.info("Verifying NIC availability...")
    result = Qemu.send_serial_command("ip link show eth0")

    # Check if the NIC is up
    assert "state UP" in result, "NIC did not re-initialize properly after reboot."
    logger.info("NIC is available and re-initialized correctly after reboot.")

