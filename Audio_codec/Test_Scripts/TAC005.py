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

def test_mute_playback(qemu_vm):
    """
    Test muting the playback using the amixer command.
    Verifies that both left and right channels are muted after the command.
    """

    # Get a logger for this test module
    logger = logging.getLogger(__name__)

    qemu_vm.send_serial_command("alsactl init")

    # Step 1: Capture the current state of the mixer
    logging.debug("Capturing initial mixer state...")
    initial_state_command = "amixer -c 0 sget 'Master'"
    initial_state_output = qemu_vm.send_serial_command(initial_state_command)

    # Log the initial state for debugging purposes
    logging.debug("Initial Mixer State:\n%s", initial_state_output)

    # Step 2: Execute the command to mute the playback
    logging.debug("Muting playback...")
    mute_command = "amixer -c 0 sset 'Master' mute"
    mute_output = qemu_vm.send_serial_command(mute_command)

    # Log the output of the mute command for debugging purposes
    logging.debug("Mute Command Output:\n%s", mute_output)

    # Step 3: Capture the new state of the mixer after muting
    logging.debug("Capturing mixer state after muting playback...")
    updated_state_output = qemu_vm.send_serial_command(initial_state_command)

    # Log the updated state for debugging purposes
    logging.debug("Updated Mixer State:\n%s", updated_state_output)

    # Step 4: Verify the mute status of both channels
    # After muting, both channels should have [off] indicating the mute status.
    assert "Front Left: Playback 54 [73%] [-20.00dB] [off]" in updated_state_output, "Left channel was not muted."
    assert "Front Right: Playback 54 [73%] [-20.00dB] [off]" in updated_state_output, "Right channel was not muted."

    # Step 5: Log the verification
    logging.debug("Verification of the change:")
    logging.debug("Initial State:\n%s", initial_state_output)
    logging.debug("Updated State:\n%s", updated_state_output)
