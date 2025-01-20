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


def test_list_all_controls(qemu_vm):
    """
    Test listing all available audio controls using 'amixer -c 0 controls'.
    Verifies that the list contains the expected controls.
    """

    # Get a logger for this test module
    logger = logging.getLogger(__name__)

    qemu_vm.send_serial_command("alsactl init")

    # Step 1: Run the command to list all controls
    logging.debug("Listing all available audio controls...")
    command = "amixer -c 0 controls"
    output = qemu_vm.send_serial_command(command)

    # Step 2: Log the output for debugging purposes
    logging.debug("Available Audio Controls:\n%s", output)

    # Step 3: Verify that the output contains expected controls
    assert "numid=3,iface=CARD,name='Line Out Phantom Jack'" in output, "Line Out Phantom Jack not found."
    assert "numid=2,iface=MIXER,name='Master Playback Switch'" in output, "Master Playback Switch not found."
    assert "numid=1,iface=MIXER,name='Master Playback Volume'" in output, "Master Playback Volume not found."
    assert "numid=4,iface=PCM,name='Playback Channel Map'" in output, "Playback Channel Map not found."

    # Step 4: Log the verification
    logging.debug("Audio controls listing verification completed.")
