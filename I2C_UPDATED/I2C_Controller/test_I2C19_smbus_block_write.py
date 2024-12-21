import subprocess
from smbus2 import SMBus
import pytest
from Inputs.common_inputs import Inputs

"This test case is to verify I2C SMBuslock Write"

def smbus_byte_write(bus_number, device_address, register, data):

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

def unload_lm75():

    print("\nunloading lm75 module for this test")
    result = subprocess.run(['sudo', 'modprobe', '-r', 'lm75'], capture_output=True, text=True)
    return result.returncode

def load_lm75():

    print("\nTest completed Again loading  lm75")
    subprocess.run(['sudo', 'modprobe', 'lm75'], check=True)

def test_smbus_byte_write():

    unload_lm75()

    register = 0x10
    data = [0x11, 0x22, 0x33, 0x44]  # Example data to write

    success = smbus_byte_write(Inputs.I2C_BUS,Inputs.DEVICE_ADDR, register, data)
    assert success, "Failed to perform SMBus byte write operation."
    load_lm75()

if __name__ == "__main__":
    pytest.main([__file__])

