import subprocess
import pytest

def get_gpio_lines():
    # Run gpioinfo to get details about GPIO lines
    result = subprocess.run(['sudo','gpioinfo'], stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True)
    if result.returncode != 0:
        raise Exception(f"Error running gpioinfo: {result.stderr.decode()}")
    
    # Parse the output to extract line names (e.g., "dummy0")
    lines = result.stdout.decode().splitlines()
    gpio_lines = []
    
    for line in lines:
        if 'line' in line:
            parts = line.split(":")
            if len(parts) > 1:
                # Extract the GPIO line name from the second part
                try:
                    # The line name is expected between quotes, e.g., "dummy0"
                    line_name = parts[1].split('"')[1]  # Extract the name inside quotes
                    if line_name:
                        gpio_lines.append(line_name)
                except IndexError:
                    continue  # Ignore malformed lines
    return gpio_lines

def test_gpio_find():
    try:
        gpio_lines = get_gpio_lines()
        assert len(gpio_lines) >  0, "No GPIO lines found"

        # Check each GPIO line with gpiofind
        for line_name in gpio_lines:
            result = subprocess.run(['sudo','gpiofind', line_name], stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True)
            assert result.returncode == 0, f"Failed to find GPIO line {line_name}"
            print(f"GPIO line {line_name} found: {result.stdout.decode().strip()}")
    
    except Exception as e:
        pytest.fail(f"Test failed: {e}")

