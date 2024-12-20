import subprocess
import pytest

def i2c_block_write(bus_number, device_address, register, data):
    """
    Perform an I2C block write operation.
    :param bus_number: I2C bus number
    :param device_address: I2C device address (in hexadecimal)
    :param register: Register address to write to (in hexadecimal)
    :param data: List of data bytes to write to the register
    :return: Success status of the operation
    """
    try:
        # Construct the command
        data_str = ' '.join([hex(d) for d in data])
        command = f'i2cset -y -f {bus_number} {hex(device_address)} {hex(register)} {data_str} i'
        result = subprocess.run(command, shell=True, capture_output=True, text=True)
        
        # Check if the command was successful
        if result.returncode == 0:
            print(f"Block write to device {hex(device_address)} at register {hex(register)} successful.")
            return True
        else:
            print(f"Error in block write to device {hex(device_address)} at register {hex(register)}: {result.stderr.strip()}")
            return False
    except Exception as e:
        print(f"Exception occurred: {e}")
        return False

def test_i2c_block_write():
    """
    Test to verify I2C block write operation.
    """
    bus_number = 0  # Change to the appropriate bus number
    device_address = 0x48  # Example I2C address
    register = 0x10  # Example register address
    data = [0x11, 0x22, 0x33, 0x44, 0x55, 0x66, 0x77, 0x88]  # Example data to write

    success = i2c_block_write(bus_number, device_address, register, data)
    
    # Assert that the block write operation was successful
    assert success, "Failed to perform I2C block write operation."

if __name__ == "__main__":
    pytest.main([__file__])

