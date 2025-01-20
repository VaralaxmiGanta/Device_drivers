import os
import sys
import pytest
import re
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


def test_throughput(qemu_instance):
    """
    Test to measure network throughput of the NIC using iperf3.
    Steps:
        1. Install iperf3 on the server.
        2. Start iperf3 server.
        3. Run iperf3 client and connect to the server.
        4. Analyze the throughput results.
    Expected Result: Throughput should meet expectations based on network conditions.
    """
    Qemu = qemu_instance

    # Get a logger for this test module
    logger = logging.getLogger(__name__)

    server_ip = "10.0.2.15"  # Replace with the actual server IP address

    # Step 1: Install iperf3 on the server (only if it's not already installed)
    # print("Installing iperf3 on the server...")
    # Qemu.send_serial_command("apt-get update")
    # Qemu.send_serial_command("apt-get install -y iperf3")

    # Step 2: Start iperf3 server
    logger.info(f"Starting iperf3 server on {server_ip}...")
    # Qemu.send_serial_command("iperf3 -s &")

    # Correct path for file transfer
    Qemu.transfer_file("Tests/Inputs/start_sever.py", "/root/start_server.py")

    # Adjust permissions
    Qemu.send_serial_command("chmod 777 /root/start_server.py")

    # Start the server
    PID = Qemu.send_serial_command("python3 /root/start_server.py")

    # Use regular expression to find the PID
    match = re.search(r"PID: (\d+)", PID)
    process_id = match.group(1)  # Extract the first captured grou

    # Step 3: Run iperf3 client and connect to the server
    logger.info(f"Running iperf3 client to connect to server {server_ip}...")
    result = Qemu.send_serial_command(f"iperf3 -c {server_ip}")

    # Step 4: Analyze the results
    logger.info(f"iperf3 test results:\n{result}")


    # Extract throughput (bandwidth) from the result
    if "receiver" in result:
        # Extract throughput (bandwidth) from the result
        lines = result.split("\n")

        # Loop through the lines to find the receiver line and extract the throughput
        for line in lines:
            # Check if the line is not empty and if the last word is "receiver"
            if line.strip() and line.split()[-1] == "receiver":
                # Regular expression to find the number before "Mbits/sec"
                pattern = r"(\d+)\sMbits/sec"

                # Find all matches
                matches = re.findall(pattern, line)

                # Check and print the results
                if matches:
                    # Store the number and unit as variables
                    throughput = matches[-1]  # Assuming you want the last match
                    unit = "Mbits/sec"

                logger.info(f"Measured throughput: {throughput} {unit}")

                # Convert throughput to float for comparison
                throughput_value = float(throughput)

                # Assert that the throughput meets expected criteria
                assert throughput_value > 100, f"Throughput is below the expected threshold: {throughput_value} {unit}"

    Qemu.send_serial_command(f"kill {process_id}")