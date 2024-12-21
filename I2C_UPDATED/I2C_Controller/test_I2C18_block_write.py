import subprocess
import pytest
from Inputs.common_inputs import Inputs

"This test case is to verify I2C block Write"


def i2c_block_write(bus_number, device_address, register, data):
    try:
        data_str = ' '.join([hex(d) for d in data])
        command = f'i2cset -y -f {bus_number} {hex(device_address)} {hex(register)} {data_str} i'
        result = subprocess.run(command, shell=True, capture_output=True, text=True)
        
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

    register = 0x10
    data = [0x11, 0x22, 0x33, 0x44, 0x55, 0x66, 0x77, 0x88]  # Example data to write

    success = i2c_block_write(Inputs.I2C_BUS,Inputs.DEVICE_ADDR, register, data)
    
    assert success, "Failed to perform I2C block write operation."

if __name__ == "__main__":
    pytest.main([__file__])

