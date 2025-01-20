import sys
import os
import pytest
import logging

# Add the project root directory to the Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))

from Framework.Core.QemuAutomation import Actions

@pytest.fixture(scope="module")
def qemu_vm():
    """
    Fixture to start and stop QEMU VM for the test case.
    """
    qemu = Actions()
    qemu.QemuStart()
    yield qemu
    qemu.QemuStop()

def test_driver_loading(qemu_vm):
    """
    Test case to verify the NIC driver loads successfully.
    """
    # Get a logger for this test module
    logger = logging.getLogger(__name__)

    # Check if the e1000 driver is already loaded
    lsmod_output = qemu_vm.send_serial_command("lsmod | grep eth0")

    if not lsmod_output.strip():
        # Load the e1000 driver
        modprobe_output = qemu_vm.send_serial_command("modprobe e1000")
        assert "error" not in modprobe_output.lower(), "Failed to load the e1000 driver"

    # Verify module parameters with modinfo
    modinfo_output = qemu_vm.send_serial_command("modinfo e1000")
    assert "filename" in modinfo_output, "Failed to retrieve module information for e1000"
    assert "description" in modinfo_output, "Driver information is incomplete"

    # Final assertion: Check if the driver is loaded
    final_lsmod_output = qemu_vm.send_serial_command("lsmod | grep e1000")
    assert "e1000" in final_lsmod_output, "e1000 driver is not loaded"
