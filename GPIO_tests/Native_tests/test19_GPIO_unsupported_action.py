import subprocess
import pytest

GPIO_PATH = "/sys/class/gpio/dummy0/power/runtime_status"  # Path for GPIO status file

def test_gpio_action_unsupported():
    # Check the current status of the GPIO pin
    with open(GPIO_PATH, 'r') as f:
        current_status = f.read().strip()

    # If the current status is 'unsupported', any action must fail
    if "unsupported" in current_status:
        pytest.fail(f"GPIO path {GPIO_PATH} is marked as unsupported. Any further actions will fail.")
    
    # Attempt to write to the GPIO 'runtime_status' file (if it wasn't unsupported)
    result = subprocess.run(f"echo 'active' | sudo tee {GPIO_PATH}", capture_output=True, text=True, shell=True)

    # Print outputs
    print(f"stderr output: {result.stderr}")
    print(f"stdout output: {result.stdout}")
    
    # If the action resulted in permission denied, fail the test
    if "Permission denied" in result.stderr:
        pytest.fail(f"Permission denied while attempting to write to {GPIO_PATH}. Test failed.")
    
