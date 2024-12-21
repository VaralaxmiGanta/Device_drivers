import subprocess
import smbus2 as smbus
import pytest
from Inputs.common_inputs import Inputs

"This test case is to verify the temperature reading using i2c-tools"


@pytest.fixture
def register():
    return 0x00

def unload_lm75():
    print("\nunloading lm75 module for this test")
    result = subprocess.run(['sudo', 'modprobe', '-r', 'lm75'], capture_output=True, text=True)
    return result.returncode

def load_lm75():
    print("\nTest completed Again loading  lm75")
    subprocess.run(['sudo', 'modprobe', 'lm75'], check=True)

def test_read_from_i2c_device(register):

    bus = smbus.SMBus(Inputs.I2C_BUS)
    unload_lm75()
    
    try:
        # Reading one byte from the register of the I2C device
        data = bus.read_byte_data(Inputs.DEVICE_ADDR, register)
        print(f"Data read from device {Inputs.DEVICE_ADDR:#x}, register {register:#x}: {data}")
        
        # Verify the data (here we assume any byte read is valid, you can adjust this check)
        assert data is not None
    except Exception as e:
        pytest.fail(f"Failed to read from device: {e}")
    load_lm75()

