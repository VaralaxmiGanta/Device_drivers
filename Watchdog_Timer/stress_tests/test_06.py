"""Stress test for writing to the watchdog while simulating networ
k latency."""

import pytest
import os
import time
import subprocess

WATCHDOG_DEVICE_PATH = "/dev/watchdog"

@pytest.fixture
def setup_watchdog():
    if not os.path.exists(WATCHDOG_DEVICE_PATH):
        pytest.skip("Watchdog device not available")
    yield


def test_watchdog_with_network_latency(setup_watchdog):

    subprocess.run(["sudo", "tc", "qdisc", "add", "dev", "eth0", "root", "netem", "delay", "200ms"])

    with open(WATCHDOG_DEVICE_PATH, 'w') as wd:
        start_time = time.time()
        for _ in range(1000):
            wd.write("heartbeat")
            time.sleep(0.01)

    subprocess.run(["sudo", "tc", "qdisc", "del", "dev", "eth0", "root"])

    elapsed_time = time.time() - start_time
    print(f"Watchdog write with network latency took {elapsed_time:.2f} seconds")
    assert elapsed_time < 20  
