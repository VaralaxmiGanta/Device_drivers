import os
import sys
import pytest
import time
import logging

# Adding the project root directory to the Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))

from Framework.Core.QAUTO import Actions


@pytest.fixture(scope="module")
def qemu_instance():
    """Fixture to start and stop the QEMU instance."""
    Qemu = Actions()
    Qemu.QemuStart()
    yield Qemu
    Qemu.QemuStop()


def test_error_handling(qemu_instance):
    """
    Test NIC's ability to handle errors such as packet drops or collisions.
    Steps:
        1. Simulate network congestion using iperf3.
        2. Monitor NIC for errors and dropped packets.
        3. Recover from errors by stopping the iperf3 server and verify NIC recovery.
    Expected Result: NIC should report errors appropriately and recover from issues.
    """
    Qemu = qemu_instance

    # Get a logger for this test module
    logger = logging.getLogger(__name__)

    # Step 1: Simulate Network Congestion by generating high network load
    logger.info("Starting iperf3 server to simulate network congestion...")
    # Correct path for file transfer
    Qemu.transfer_file("Tests/Inputs/start_sever.py", "/root/start_server.py")

    # Adjust permissions
    Qemu.send_serial_command("chmod 777 /root/start_server.py")

    # Start the server
    PID = Qemu.send_serial_command("python3 /root/start_server.py")

    # Simulate client load by running iperf3 on the client
    logger.info("Starting iperf3 client to generate traffic...")
    iperf3_result = Qemu.send_serial_command("iperf3 -c 10.0.2.15")

    # Step 2: Monitor NIC for errors and dropped packets
    logger.info("Monitoring NIC errors and dropped packets...")
    ifconfig_output = Qemu.send_serial_command("ifconfig eth0")

    # Check for packet drops or errors in the output
    assert "RX errors" not in ifconfig_output, "Received errors detected."
    assert "TX errors" not in ifconfig_output, "Transmission errors detected."
    assert "dropped" not in ifconfig_output, "Dropped packets detected."

    logger.info("NIC error and drop check passed.")

    # Step 3: Recover from errors by stopping the iperf3 server and monitoring recovery
    logger.info("Stopping iperf3 server...")
    Qemu.send_serial_command("pkill iperf3")  # Stop the iperf3 server

    # Allow time for recovery
    time.sleep(5)

    # Recheck if there are errors or dropped packets after recovery
    ifconfig_output_after_recovery = Qemu.send_serial_command("ifconfig eth0")

    assert "RX errors" not in ifconfig_output_after_recovery, "Received errors detected after recovery."
    assert "TX errors" not in ifconfig_output_after_recovery, "Transmission errors detected after recovery."
    assert "dropped" not in ifconfig_output_after_recovery, "Dropped packets detected after recovery."

    logger.info("NIC recovery successful, no further errors or packet drops detected.")
