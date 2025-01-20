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


def test_list_all_simple_controls(qemu_vm):
    """
    Test listing all simple mixer controls using 'amixer -c 0 scontrols'.
    Verifies that the simple mixer control is listed correctly.
    """

    # Get a logger for this test module
    logger = logging.getLogger(__name__)

    qemu_vm.send_serial_command("alsactl init")

    # Step 1: Run the command to list all simple controls
    logging.debug("Listing all simple mixer controls...")
    command = "amixer -c 0 scontrols"
    output = qemu_vm.send_serial_command(command)

    # Step 2: Log the output for debugging purposes
    logging.debug("Available Simple Mixer Controls:\n%s", output)

    # Step 3: Verify that the output contains the 'Master' simple control
    assert "Simple mixer control 'Master',0" in output, "'Master' control not found in simple mixer controls."

    # Step 4: Log the verification
    logging.debug("Simple mixer control listing verification completed.")
