import subprocess
import pytest

@pytest.fixture
def i2c_functionality():
    """
    Run the `i2cdetect -F` command and return its output.
    """
    bus_number = 0  # Change this if you are using a different I2C bus
    try:
        result = subprocess.run(
            ["i2cdetect", "-F", str(bus_number)],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            check=True
        )
        return result.stdout
    except subprocess.CalledProcessError as e:
        pytest.fail(f"Command failed with error: {e.stderr}")

@pytest.mark.parametrize("feature", [
    "SMBus Quick Command",
    "SMBus Send Byte",
    "SMBus Receive Byte",
    "SMBus Write Byte",
    "SMBus Read Byte",
    "SMBus Write Word",
    "SMBus Read Word",
    "SMBus Block Write",
    "SMBus Block Read",
])
def test_smbus_support(i2c_functionality, feature):
    """
    Test if the I2C adapter supports the required SMBus functionalities.
    """
    output = i2c_functionality
    lines = output.splitlines()

    # Look for the feature line in the output
    for line in lines:
        if feature in line:
            assert "yes" in line, f"{feature} is not supported"
            break
    else:
        pytest.fail(f"Feature '{feature}' not found in output")

if __name__ == "__main__":
    pytest.main(["-v", __file__])

