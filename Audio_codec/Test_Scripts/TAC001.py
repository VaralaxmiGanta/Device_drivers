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

def test_set_volume_to_50_with_change_verification(qemu_vm):
    """
    Test setting the volume to 50% using the amixer command.
    Verifies the change in volume by comparing the mixer states before and after the command.
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

    # Step 2: Execute the command to set the volume to 50%
    logging.debug("Setting volume to 50%...")
    set_volume_command = "amixer -c 0 sset 'Master' 50%"
    set_volume_output = qemu_vm.send_serial_command(set_volume_command)

    # Log the output of the volume-setting command for debugging purposes
    logging.debug("Set Volume Command Output:\n%s", set_volume_output)

    # Step 3: Capture the new state of the mixer after setting the volume
    logging.debug("Capturing mixer state after setting volume...")
    updated_state_output = qemu_vm.send_serial_command(initial_state_command)

    # Log the updated state for debugging purposes
    logging.debug("Updated Mixer State:\n%s", updated_state_output)

    # Step 4: Verify changes in the mixer state
    # Initial state should not have 50% for both channels
    assert "Front Left: Playback 37 [50%]" not in initial_state_output, "Initial state should not have 50% volume."
    assert "Front Right: Playback 37 [50%]" not in initial_state_output, "Initial state should not have 50% volume."

    # Updated state should have 50% for both channels
    assert "Front Left: Playback 37 [50%]" in updated_state_output, "Volume for Front Left channel not set to 50%."
    assert "Front Right: Playback 37 [50%]" in updated_state_output, "Volume for Front Right channel not set to 50%."

    # Step 5: Verify the actual change
    logging.debug("Verification of the change:")
    logging.debug("Initial State:\n%s", initial_state_output)
    logging.debug("Updated State:\n%s", updated_state_output)
