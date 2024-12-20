import subprocess
import pytest

def i2c_dump(bus_number, device_address):
    try:
        # Execute the i2cdump command
        command = ['i2cdump', '-y', str(bus_number), hex(device_address)]
        result = subprocess.run(command, capture_output=True, text=True)
        
        # Check if the command was successful
        if result.returncode == 0:
            print(f"Data dump from device {hex(device_address)}:\n{result.stdout}")
            return result.stdout
        else:
            print(f"Error dumping data from device {hex(device_address)}: {result.stderr.strip()}")
            return None
    except Exception as e:
        print(f"Exception occurred: {e}")
        return None

def test_i2c_dump():
    bus_number = 0  # Change to the appropriate bus number
    device_address = 0x48  # Example I2C address

    dump_data = i2c_dump(bus_number, device_address)
    
    # Assert that the data dump was successful
    assert dump_data is not None, "Failed to dump data from the I2C device."

if __name__ == "__main__":
    pytest.main([__file__])

