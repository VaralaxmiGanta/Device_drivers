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


def test_query_current_settings(qemu_vm):
    """
    Test querying the current settings of the 'Master' mixer control.
    Verifies that the current volume and mute state are displayed correctly.
    """

    # Get a logger for this test module
    logger = logging.getLogger(__name__)

    qemu_vm.send_serial_command("alsactl init")

    # Step 1: Run the command to query current settings
    logging.debug("Querying current mixer settings...")
    command = "amixer -c 0 sget 'Master'"
    output = qemu_vm.send_serial_command(command)

    # Step 2: Log the output for debugging purposes
    logging.debug("Current Mixer Settings:\n%s", output)

    # Step 3: Verify that the output contains expected information
    assert "Simple mixer control 'Master',0" in output, "Incorrect mixer control name."
    assert "Front Left: Playback 54 [73%] [-20.00dB] [on]" in output, "Left channel settings not as expected."
    assert "Front Right: Playback 54 [73%] [-20.00dB] [on]" in output, "Right channel settings not as expected."

    # Step 4: Log the verification
    logging.debug("Mixer settings verification completed.")
