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

def test_nic_network_connection(qemu_vm):
    """
    Test case to verify NIC establishes a working network connection.
    """

    # Get a logger for this test module
    logger = logging.getLogger(__name__)

    # Sending serial commands to check and configure the NIC inside the QEMU VM
    command_output = qemu_vm.send_serial_command("ip link show")
    logger.info("adding ip address to the eth0")
    qemu_vm.send_serial_command("ip addr add 192.168.122.1/24 dev eth0")
    qemu_vm.send_serial_command("ip link set eth0 up")

    # Test connectivity with a reachable host (for example 192.168.122.1)
    logger.info("verifing the connection with the added IP address using ping command")
    ping_output = qemu_vm.send_serial_command("ping -c 4 192.168.122.1")

    # Check the NIC status and assert
    assert "eth0" in command_output and "state UP" in command_output.split("eth0", 1)[1], "The NIC didn't establishes a working network connection"
    assert "Destination Host Unreachable" not in ping_output, "Ping failed - No network connectivity"
