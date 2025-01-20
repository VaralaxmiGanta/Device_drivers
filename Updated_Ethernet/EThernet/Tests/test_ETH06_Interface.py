import subprocess
import pytest
from Inputs.common_inputs import Inputs

"This test case is to verify the status of eth0 interface"

def get_interface_status(interface_name):
    result = subprocess.run(['ip', 'link', 'show', interface_name], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    if result.returncode != 0:
        return f"Failed to get status for interface {interface_name}"
    
    return 'UP' if 'UP' in result.stdout else 'DOWN'

def test_eth0_status():
    status = get_interface_status(Inputs.Interface)
    assert status in ['UP', 'DOWN'], f"Unexpected status: {status}"
    print(f"Interface eth0 is {status}.")
