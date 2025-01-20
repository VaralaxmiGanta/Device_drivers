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

def test_toggle_mute_state(qemu_vm):
    """
    Test toggling the mute state of the playback using the amixer command.
    Verifies that the mute state toggles (if muted, it becomes unmuted, and vice versa).
    """

    # Get a logger for this test module
    logger = logging.getLogger(__name__)

    qemu_vm.send_serial_command("alsactl init")

    # Step 1: Capture the initial state of the mixer
    logging.debug("Capturing initial mixer state...")
    initial_state_command = "amixer -c 0 sget 'Master'"
    initial_state_output = qemu_vm.send_serial_command(initial_state_command)

    # Log the initial state for debugging purposes
    logging.debug("Initial Mixer State:\n%s", initial_state_output)

    # Step 2: Run the toggle command
    logging.debug("Toggling mute state...")
    toggle_command = "amixer -c 0 sset 'Master' toggle"
    toggle_output = qemu_vm.send_serial_command(toggle_command)

    # Log the output of the toggle command for debugging purposes
    logging.debug("Toggle Command Output:\n%s", toggle_output)

    # Step 3: Capture the new state of the mixer after toggling
    logging.debug("Capturing mixer state after toggling mute state...")
    updated_state_output = qemu_vm.send_serial_command(initial_state_command)

    # Log the updated state for debugging purposes
    logging.debug("Updated Mixer State:\n%s", updated_state_output)

    # Step 4: Verify that the mute state has toggled correctly
    # Before toggling, both channels should be "on"
    # After toggling, both channels should be "off"
    if "Front Left: Playback 54 [73%] [-20.00dB] [on]" in initial_state_output:
        assert "Front Left: Playback 54 [73%] [-20.00dB] [off]" in updated_state_output, "Left channel did not toggle correctly."
        assert "Front Right: Playback 54 [73%] [-20.00dB] [off]" in updated_state_output, "Right channel did not toggle correctly."
    else:
        assert "Front Left: Playback 54 [73%] [-20.00dB] [on]" in updated_state_output, "Left channel did not toggle correctly."
        assert "Front Right: Playback 54 [73%] [-20.00dB] [on]" in updated_state_output, "Right channel did not toggle correctly."

    # Step 5: Log the verification
    logging.debug("Verification of the change:")
    logging.debug("Initial State:\n%s", initial_state_output)
    logging.debug("Updated State:\n%s", updated_state_output)
