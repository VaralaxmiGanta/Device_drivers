from smbus2 import SMBus
import pytest

def smbus_byte_write(bus_number, device_address, register, data):
    """
    Perform an SMBus byte write operation.
    :param bus_number: I2C bus number
    :param device_address: I2C device address
    :param register: Register address to write to
    :param data: List of data bytes to write to the register
    :return: Success status of the operation
    """
    try:
        with SMBus(bus_number) as bus:
            for byte in data:
                bus.write_byte_data(device_address, register, byte)
                register += 1
            print(f"Byte write to device {hex(device_address)} at register {hex(register)} successful.")
            return True
    except Exception as e:
        print(f"Exception occurred: {e}")
        return False

def test_smbus_byte_write():
    """
    Test to verify SMBus byte write operation.
    """
    bus_number = 0  # Change to the appropriate bus number
    device_address = 0x48  # Example I2C address
    register = 0x10  # Example register address
    data = [0x11, 0x22, 0x33, 0x44]  # Example data to write

    success = smbus_byte_write(bus_number, device_address, register, data)
    
    # Assert that the byte write operation was successful
    assert success, "Failed to perform SMBus byte write operation."

if __name__ == "__main__":
    pytest.main([__file__])

