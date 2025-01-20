import sys
import os
import pytest
import logging

# Adding the project root directory to the Python path
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


def test_advanced_set_volume_by_numid(qemu_vm):
    """
    Test setting the volume using the numid (advanced set volume).
    Verifies that the volume for the control with numid=1 is set to 50%.
    """

    # Get a logger for this test module
    logger = logging.getLogger(__name__)

    qemu_vm.send_serial_command("alsactl init")

    # Step 1: Run the command to set the volume to 50% using numid=1
    logging.debug("Setting volume for numid=1 to 50%...")
    command = "amixer -c 0 cset numid=1 50%"
    output =  qemu_vm.send_serial_command(command)

    # Step 2: Log the output for debugging purposes
    logging.debug("Output after setting volume to 50%%:\n%s", output)

    # Step 3: Verify the volume setting
    assert "values=37,37" in output, "Failed to set volume to 50%."
    command = "amixer -c 0 cset numid=1 73%"
    qemu_vm.send_serial_command(command)

    # Step 4: Log the verification
    logging.debug("Volume setting to 50%% verified.")
