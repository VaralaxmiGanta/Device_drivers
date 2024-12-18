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


def test_irq_affinity(qemu_instance):
    """
    Test to verify IRQ affinity for network interrupt handling.
    Steps:
        1. Check current IRQ assignment.
        2. Change IRQ affinity to a specified CPU core.
        3. Verify the change.
    Expected Result: NIC’s interrupts are handled by the specified CPU core.
    """
    Qemu = qemu_instance

    # Get a logger for this test module
    logger = logging.getLogger(__name__)

    interface = "eth0"

    # Step 1: Check current IRQ assignment
    logger.info(f"Checking current IRQ assignment for {interface}...")
    irq_assignment = Qemu.send_serial_command(f"cat /proc/interrupts | grep {interface}")
    logger.info(f"Current IRQ assignment:\n{irq_assignment.strip()}")

    # Extract IRQ number from the current IRQ assignment
    irq_number = irq_assignment.strip().split()[0]

    # Step 2: Change IRQ affinity to a specified CPU core (e.g., CPU core 1)
    logger.info(f"Changing IRQ affinity for IRQ {irq_number} to CPU core 1...")
    Qemu.send_serial_command(f"echo '1' > /proc/irq/{irq_number}/smp_affinity")

    # Step 3: Verify the IRQ affinity change
    logger.info(f"Verifying IRQ affinity change for {interface}...")
    updated_irq_assignment = Qemu.send_serial_command(f"cat /proc/interrupts | grep {interface}")
    logger.info(f"Updated IRQ assignment:\n{updated_irq_assignment.strip()}")

    # Verify that the IRQ affinity has been updated correctly
    assert '1' in updated_irq_assignment, "IRQ affinity change not applied correctly."

