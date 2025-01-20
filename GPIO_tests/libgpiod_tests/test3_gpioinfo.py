import subprocess
import pytest

def test_gpio_info():
    try:
        result = subprocess.run(['sudo','gpioinfo'], stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True)
        print("found the below gpio information: ")
        print(result)
        assert result.returncode == 0, f"Error fetching GPIO info: {result.stderr.decode()}"
        assert 'gpiochip' in result.stdout.decode(), "Expected gpiochip0 not found in the output"
    except subprocess.CalledProcessError as e:
        pytest.fail(f"Error running gpioinfo: {e}")

