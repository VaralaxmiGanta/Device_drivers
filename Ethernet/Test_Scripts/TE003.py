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

def test_driver_unloading(qemu_instance):
    """
    Test to verify the NIC driver can be unloaded safely.
    Steps:
        1. Unload the driver using `modprobe -r e1000`.
        2. Check if the module is unloaded using `lsmod | grep e1000`.
    Expected Result: The driver unloads cleanly and the NIC is unavailable.
    """
    Qemu = qemu_instance

    # Get a logger for this test module
    logger = logging.getLogger(__name__)

    # Step 1: Unload the NIC driver
    unload_output = Qemu.send_serial_command("modprobe -r e1000")
    assert "error" not in unload_output.lower(), "Failed to unload e1000 driver."

    # Step 2: Check if the module is unloaded
    lsmod_output = Qemu.send_serial_command("lsmod | grep e1000")
    assert not lsmod_output.strip(), "e1000 driver is still loaded."

