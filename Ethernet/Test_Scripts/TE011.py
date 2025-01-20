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


def test_vlan_support(qemu_instance):
    """
    Test to verify NIC supports VLAN tagging and operates with VLANs.
    Steps:
        1. Create a VLAN interface.
        2. Assign an IP address to the VLAN interface and bring it up.
        3. Test connectivity within the VLAN using ping.
        4. Remove the VLAN interface.
    Expected Result: NIC correctly handles VLAN tagging and communicates within the VLAN.
    """
    Qemu = qemu_instance

    # Get a logger for this test module
    logger = logging.getLogger(__name__)

    vlan_id = 100
    vlan_interface = f"eth0.{vlan_id}"
    vlan_ip = "192.168.122.0"
    vlan_gateway = "192.168.122.1"  # Replace with the reachable device in VLAN 100

    # Step 1: Create a VLAN interface
    logger.info(f"Creating VLAN interface {vlan_interface}...")
    Qemu.send_serial_command(f"ip link add link eth0 name {vlan_interface} type vlan id {vlan_id}")

    # Verify VLAN interface creation
    vlan_result = Qemu.send_serial_command("ip link show")
    logger.info(f"VLAN interface creation output:\n{vlan_result.strip()}")
    assert vlan_interface in vlan_result, f"Failed to create VLAN interface {vlan_interface}."

    # Step 2: Assign IP address to the VLAN interface and bring it up
    logger.info(f"Assigning IP address {vlan_ip}/24 to {vlan_interface} and bringing it up...")
    Qemu.send_serial_command(f"ip addr add {vlan_ip}/24 dev {vlan_interface}")
    Qemu.send_serial_command(f"ip link set {vlan_interface} up")

    # Verify IP address assignment
    ip_result = Qemu.send_serial_command(f"ip addr show {vlan_interface}")
    logger.info(f"IP address assignment output:\n{ip_result.strip()}")
    assert vlan_ip in ip_result, f"Failed to assign IP address {vlan_ip} to {vlan_interface}."

    # Step 3: Test connectivity within the VLAN
    logger.info(f"Testing connectivity to VLAN gateway {vlan_gateway}...")
    ping_result = Qemu.send_serial_command(f"ping -c 4 {vlan_gateway}")
    logger.info(f"Ping result:\n{ping_result.strip()}")
    assert "0% packet loss" in ping_result, f"Failed to communicate within VLAN {vlan_id}."

    # Step 4: Remove the VLAN interface
    logger.info(f"Removing VLAN interface {vlan_interface}...")
    Qemu.send_serial_command(f"ip link delete {vlan_interface}")

    # Verify VLAN interface removal
    vlan_removal_result = Qemu.send_serial_command("ip link show")
    logger.info(f"VLAN interface removal output:\n{vlan_removal_result.strip()}")
    assert vlan_interface not in vlan_removal_result, f"Failed to remove VLAN interface {vlan_interface}."
