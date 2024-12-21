import subprocess
import pytest
from Inputs.common_inputs import Inputs


"This test case is to verify I2C block read"

def i2c_dump(bus_number, device_address):
    try:
        command = ['i2cdump', '-y', str(bus_number), hex(device_address)]
        result = subprocess.run(command, capture_output=True, text=True)
        
        if result.returncode == 0:
            print(f"Data dump from device {hex(device_address)}:\n{result.stdout}")
            return result.stdout
        else:
            print(f"Error dumping data from device {hex(device_address)}: {result.stderr.strip()}")
            return None

    except Exception as e:
        print(f"Exception occurred: {e}")
        return None

def unload_lm75():
    print("\nunloading lm75 module for this test")
    result = subprocess.run(['sudo', 'modprobe', '-r', 'lm75'], capture_output=True, text=True)
    return result.returncode

def load_lm75():
    print("\nTest completed Again loading  lm75")
    subprocess.run(['sudo', 'modprobe', 'lm75'], check=True)

def test_i2c_dump():

    unload_lm75()
    dump_data = i2c_dump(Inputs.I2C_BUS,Inputs.DEVICE_ADDR)
    
    # Assert that the data dump was successful
    assert dump_data is not None, "Failed to dump data from the I2C device."
    load_lm75()

if __name__ == "__main__":
    pytest.main([__file__])

