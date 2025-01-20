import subprocess
import pytest

GPIO_PIN = 999  # Invalid GPIO pin number

def test_invalid_gpio_pin():
    result = subprocess.run(f"echo {GPIO_PIN} | sudo tee /sys/class/gpio/export", capture_output=True, text=True, shell=True)

    print(f"stderr output: {result.stderr}")
    
    # If an invalid argument error is found, we make the test fail
    if "Invalid argument" in result.stderr:
        pytest.fail(f"GPIO Pin {GPIO_PIN} is invalid. Test failed due to invalid GPIO pin.")

