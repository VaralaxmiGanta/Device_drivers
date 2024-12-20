import smbus2 as smbus  # Change this to use smbus2 instead of smbus
import pytest

# Fixture for the I2C bus number
@pytest.fixture
def bus_number():
    return 0  # For example, bus 0 (adjust as needed)

# Fixture for the I2C device address
@pytest.fixture
def device_address():
    return 0x48  # Adjust to the actual device address

# Fixture for the register to read from
@pytest.fixture
def register():
    return 0x00  # Adjust to the actual register to read from

def test_read_from_i2c_device(bus_number, device_address, register):
    bus = smbus.SMBus(bus_number)
    
    try:
        # Reading one byte from the register of the I2C device
        data = bus.read_byte_data(device_address, register)
        print(f"Data read from device {device_address:#x}, register {register:#x}: {data}")
        
        # Verify the data (here we assume any byte read is valid, you can adjust this check)
        assert data is not None
    except Exception as e:
        pytest.fail(f"Failed to read from device: {e}")

