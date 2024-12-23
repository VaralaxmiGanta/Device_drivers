import subprocess
import time
import pytest
from Inputs.common_inputs import Inputs

"""THis test case is to verify whether the network driver e1000 correctly handles interrupt  when the traffic is generated"""

# Function to get current interrupt count for a given interface
def get_interrupt_count(interface):
    result = subprocess.run(
        ["cat", "/proc/interrupts"], stdout=subprocess.PIPE, text=True
    )
    for line in result.stdout.splitlines():
        if interface in line:
            return int(line.split()[1])
    return 0

@pytest.fixture
def setup_network_traffic():
    """Simulate network traffic to generate interrupts"""
    # Start ping to generate traffic
    ping_process = subprocess.Popen(["ping", "-c", "20", "8.8.8.8"])
    yield ping_process
    ping_process.terminate()

def test_e1000_interrupt_handling(setup_network_traffic):
    """Test the interrupt handling for the e1000 driver"""
    interface = Inputs.Interface
    
    # Step 1: Record the initial interrupt count
    initial_interrupts = get_interrupt_count(interface)
    print(f"\nInitial interrupt count for {interface}: {initial_interrupts}")
    
    # Step 2: Wait for traffic to generate interrupts
    time.sleep(5)  # Allow time for interrupts to accumulate
    
    # Step 3: Record the interrupt count after generating traffic
    final_interrupts = get_interrupt_count(interface)
    print(f"Final interrupt count for {interface}: {final_interrupts}")
    
    # Step 4: Assert that interrupts were handled (the count should increase)
    assert final_interrupts > initial_interrupts, "Interrupt handling failed or no interrupts were triggered"
    

