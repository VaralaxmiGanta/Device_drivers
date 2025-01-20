import re
import os
import sys
import pytest
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


def test_jitter(qemu_instance):
    """
    Test NIC's ability to maintain low jitter (variance in round-trip time).
    Steps:
        1. Use ping with a 0.2-second interval to test jitter.
        2. Analyze the round-trip time variation from the ping results.
    Expected Result: Jitter (variance in round-trip time) should be minimal.
    """
    Qemu = qemu_instance

    # Get a logger for this test module
    logger = logging.getLogger(__name__)

    target_ip = "192.168.122.1"  # Replace with actual target IP for your environment

    # Step 1: Use ping to measure round-trip time with 0.2-second interval
    logger.info(f"Starting ping test with 0.2-second interval to {target_ip}...")
    ping_result = Qemu.send_serial_command(f"ping -i 0.2 {target_ip} -c 100")  # 100 pings

    # Step 2: Parse the ping results to check round-trip time variance
    logger.info("Analyzing ping results for jitter...")
    round_trip_times = re.findall(r'time=(\d+\.\d+)', ping_result)

    # Ensure we have collected round-trip time values
    assert len(round_trip_times) > 0, "No round-trip times found in ping results."

    # Convert the round-trip times to floats
    round_trip_times = [float(time) for time in round_trip_times]

    # Calculate the jitter (variance in round-trip time)
    min_rtt = min(round_trip_times)
    max_rtt = max(round_trip_times)
    avg_rtt = sum(round_trip_times) / len(round_trip_times)

    jitter = max_rtt - min_rtt

    # Print the results
    logger.info(f"Min RTT: {min_rtt} ms")
    logger.info(f"Max RTT: {max_rtt} ms")
    logger.info(f"Avg RTT: {avg_rtt} ms")
    logger.info(f"Jitter (max-min RTT): {jitter} ms")

    # Step 3: Assert that jitter is minimal (adjust the threshold as needed)
    assert jitter < 10, f"Jitter too high: {jitter} ms. Expected minimal variance."

    logger.info("Jitter test passed, variance in round-trip time is minimal.")
