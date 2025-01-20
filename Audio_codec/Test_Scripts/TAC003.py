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

def test_increase_volume_by_5(qemu_vm):
    """
    Test increasing the volume by 5% using the amixer command.
    Verifies that both left and right channels' volume is increased by 5%.
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

    # Step 2: Execute the command to increase the volume by 5%
    logging.debug("Increasing volume by 5%...")
    increase_volume_command = "amixer -c 0 sset 'Master' 5%+"
    increase_volume_output = qemu_vm.send_serial_command(increase_volume_command)

    # Log the output of the volume-increase command for debugging purposes
    logging.debug("Increase Volume Command Output:\n%s", increase_volume_output)

    # Step 3: Capture the new state of the mixer after increasing the volume
    logging.debug("Capturing mixer state after increasing volume by 5%...")
    updated_state_output = qemu_vm.send_serial_command(initial_state_command)

    # Log the updated state for debugging purposes
    logging.debug("Updated Mixer State:\n%s", updated_state_output)

    # Step 4: Verify the volume increase of 5%
    # We know that the initial volume was 54 (73%), and after the increase, it should be 58 (78%).
    assert "Front Left: Playback 58 [78%]" in updated_state_output, "Left channel volume was not increased by 5%."
    assert "Front Right: Playback 58 [78%]" in updated_state_output, "Right channel volume was not increased by 5%."

    # Step 5: Log the verification
    logging.debug("Verification of the change:")
    logging.debug("Initial State:\n%s", initial_state_output)
    logging.debug("Updated State:\n%s", updated_state_output)
