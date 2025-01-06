import os
import subprocess
import pytest

# Path to the control file
CONTROL_FILE = "/sys/class/gpio/dummy0/power/control"

@pytest.fixture(scope="function")
def check_control_file():
    if not os.path.exists(CONTROL_FILE):
        pytest.skip(f"{CONTROL_FILE} does not exist. Skipping test.")

def test_set_control_value(check_control_file, value="on"):
    try:
        # Set the value
        subprocess.run(["sudo", "tee", CONTROL_FILE], text=True, input=value, check=True)
        # Read back the value
        with open(CONTROL_FILE, "r") as file:
            current_value = file.read().strip()
        # Verify the value
        assert current_value == value, f"Expected {value}, got {current_value}"
        print(f"Control value set and verified as: {value}")
    except Exception as e:
        pytest.fail(f"Test failed with error: {e}")

if __name__ == "__main__":
    pytest.main(["-s", __file__])

