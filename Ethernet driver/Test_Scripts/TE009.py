import os
import sys
import pytest
import time
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

def test_interrupt_handling(qemu_instance):
    """
    Test to verify NIC generates interrupts correctly.
    Steps:
        1. Monitor the initial interrupt count using `cat /proc/interrupts | grep e1000`.
        2. Generate traffic using `ping -c 100 192.168.1.1`.
        3. Check the interrupt count again using `cat /proc/interrupts | grep e1000`.
    Expected Result: Interrupt count increases with traffic.
    """
    Qemu = qemu_instance

    # Get a logger for this test module
    logger = logging.getLogger(__name__)

    # Step 1: Monitor the initial interrupt count
    initial_interrupts = Qemu.send_serial_command("cat /proc/interrupts | grep eth0")
    logger.info(f"Initial Interrupt Count:\n{initial_interrupts.strip()}")

    # Step 2: Generate traffic using ping command
    logger.info("Generating traffic with ping...")
    Qemu.send_serial_command("ping -c 100 192.168.122.1")

    # Wait a few seconds to allow for interrupt count to update
    time.sleep(2)

    # Step 3: Check interrupt count again
    new_interrupts = Qemu.send_serial_command("cat /proc/interrupts | grep eth0")
    logger.info(f"New Interrupt Count:\n{new_interrupts.strip()}")

    # Assert the interrupt count has increased
    initial_count = int(initial_interrupts.split()[1])
    new_count = int(new_interrupts.split()[1])
    assert new_count > initial_count, f"Expected interrupt count to increase, but it didn't. Initial: {initial_count}, New: {new_count}"
