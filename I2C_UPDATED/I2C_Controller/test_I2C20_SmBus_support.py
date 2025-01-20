import subprocess
import pytest
from Inputs.common_inputs import Inputs

"This test case is to verify SMBus protocol support for I2C device"

@pytest.fixture
def i2c_functionality():

    try:
        result = subprocess.run(
            ["i2cdetect", "-F", str(Inputs.I2C_BUS)],
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

