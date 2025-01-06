import subprocess
import pytest

def test_gpio_chip_detection():
    try:
        # Run gpiodetect command to list the available GPIO chips
        result = subprocess.run(['sudo','gpiodetect'], stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True)
        
        # Ensure the command ran successfully
        assert result.returncode == 0, f"Error detecting GPIO chips: {result.stderr.decode()}"
        
        # Check if there is any GPIO chip listed in the output
        output = result.stdout.decode()
        assert 'gpiochip' in output, "No GPIO chip found in the output"
        
        # Optionally, print the output for manual verification
        print("Detected GPIO chips:")
        print(output)
        
    except subprocess.CalledProcessError as e:
        pytest.fail(f"Error running gpiodetect: {e}")

