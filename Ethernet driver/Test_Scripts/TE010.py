import pytest
import os
import sys
import logging

# Add the project root directory to the Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))

from Framework.Core.QAUTO import Actions

@pytest.fixture(scope="module")
def qemu_instance():
    """Fixture to start and stop the QEMU instance."""
    Qemu = Actions()
    Qemu.QemuStart()
    yield Qemu
    Qemu.QemuStop()

def test_mtu_size(qemu_instance):
    """
    Test to verify NIC behavior with different MTU sizes.
    Steps:
        1. Set a new MTU size (e.g., 9000 for jumbo frames).
        2. Test connectivity with the new MTU using ping.
        3. Restore the default MTU size (1500).
    Expected Result: NIC handles MTU changes without issues.
    """

    # Get a logger for this test module
    logger = logging.getLogger(__name__)

    Qemu = qemu_instance
    test_ip = "192.168.122.1"

    # Step 1: Set a new MTU size (9000 for jumbo frames)
    logger.info("Setting MTU to 9000...")
    Qemu.send_serial_command("ip link set eth0 mtu 9000")

    # Verify the MTU change
    mtu_result = Qemu.send_serial_command("ip link show eth0")
    logger.info(f"MTU after change:\n{mtu_result.strip()}")
    assert "mtu 9000" in mtu_result, "Failed to set MTU to 9000."

    # Step 2: Test connectivity with the new MTU
    logger.info("Testing connectivity with jumbo frames...")
    ping_result = Qemu.send_serial_command(f"ping -M do -s 8972 -c 4 {test_ip}")
    logger.info(f"Ping result:\n{ping_result.strip()}")
    assert "0% packet loss" in ping_result, "Ping failed with MTU 9000."

    # Step 3: Restore the default MTU size (1500)
    logger.info("Restoring default MTU (1500)...")
    Qemu.send_serial_command("ip link set eth0 mtu 1500")

    # Verify the MTU reset
    mtu_reset_result = Qemu.send_serial_command("ip link show eth0")
    logger.info(f"MTU after reset:\n{mtu_reset_result.strip()}")
    assert "mtu 1500" in mtu_reset_result, "Failed to reset MTU to 1500."
