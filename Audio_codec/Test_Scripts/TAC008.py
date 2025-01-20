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


def test_set_volume_in_dB(qemu_vm):
    """
    Test setting the volume in dB using the amixer command.
    Verifies that the volume is reduced by 10dB or increased by 10dB correctly.
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

    # Step 2: Run the command to reduce the volume by 10dB
    logging.debug("Reducing volume by 10dB...")
    volume_command = "amixer -c 0 sset 'Master' -- -10dB"
    volume_output = qemu_vm.send_serial_command(volume_command)

    # Log the output of the volume change for debugging purposes
    logging.debug("Volume Change Command Output:\n%s", volume_output)

    # Step 3: Capture the new state of the mixer after changing the volume
    logging.debug("Capturing mixer state after changing volume...")
    updated_state_output = qemu_vm.send_serial_command(initial_state_command)

    # Log the updated state for debugging purposes
    logging.debug("Updated Mixer State:\n%s", updated_state_output)

    # Step 4: Verify that the volume has been reduced by 10dB
    # Before changing the volume, the dB should be -20.00dB
    # After reducing by 10dB, it should be -10.00dB
    assert "Front Left: Playback 54 [73%] [-20.00dB] [on]" in initial_state_output, "Left channel did not start at -20.00dB."
    assert "Front Right: Playback 54 [73%] [-20.00dB] [on]" in initial_state_output, "Right channel did not start at -20.00dB."

    # Verify the new state after reducing volume by 10dB
    assert "Front Left: Playback 64 [86%] [-10.00dB] [on]" in updated_state_output, "Left channel did not reduce correctly to -10.00dB."
    assert "Front Right: Playback 64 [86%] [-10.00dB] [on]" in updated_state_output, "Right channel did not reduce correctly to -10.00dB."

    # Step 5: Log the verification
    logging.debug("Verification of the volume change:")
    logging.debug("Initial State:\n%s", initial_state_output)
    logging.debug("Updated State:\n%s", updated_state_output)
