import os
import sys
import pytest
import logging

# Add the project root directory to the Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))

from Framework.Core.QemuAutomation import Actions

@pytest.fixture(scope="module")
def qemu_instance():
    """Fixture to start and stop the QEMU instance."""
    Qemu = Actions()
    Qemu.QemuStart()
    yield Qemu
    Qemu.QemuStop()

def test_link_state(qemu_instance):
    """
    Test to verify the NIC's link state (up/down).
    Steps:
        1. Check the initial link state using `ethtool eth0`.
        2. Manually bring the link-up using `ip link set eth0 up`.
        3. Verify the link state again using `ethtool eth0`.
    Expected Result: Link state changes as expected.
    """
    Qemu = qemu_instance

    # Get a logger for this test module
    logger = logging.getLogger(__name__)

    # Step 1: Check the initial link state
    initial_state = Qemu.send_serial_command("ethtool eth0 | grep 'Link detected'")
    assert initial_state, "Failed to get link state for eth0."
    initial_state = "yes" if "yes" in initial_state.lower() else "no"

    # Step 2: Bring the link-up
    Qemu.send_serial_command("ip link set eth0 up")
    link_up_state = Qemu.send_serial_command("ethtool eth0 | grep 'Link detected'")
    assert link_up_state, "Failed to get link state after bringing the link up."
    assert "yes" in link_up_state.lower(), "Link state did not change to 'up'."

    # Step 3: Optionally bring the link down (if needed)
    # Qemu.send_serial_command("ip link set eth0 down")
    # link_down_state = Qemu.send_serial_command("ethtool eth0 | grep 'Link detected'")
    # assert link_down_state, "Failed to get link state after bringing the link down."
    # assert "no" in link_down_state.lower(), "Link state did not change to 'down'."
