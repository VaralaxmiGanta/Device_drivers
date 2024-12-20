import subprocess
import pytest

def read_incorrect_i2c_address(bus_number, address):
    print(f"Attempting to read from incorrect I2C address {address} on bus {bus_number}...")
    result = subprocess.run(['sudo', 'i2cget', '-y', str(bus_number), str(address)], capture_output=True, text=True)
    return result.returncode, result.stdout, result.stderr

def test_incorrect_i2c_address():
    bus_number = 0  
    incorrect_address = 0x77  # Use an address that doesn't exist on the bus
    print("\nStarting test for reading from incorrect I2C address...")
    returncode, stdout, stderr = read_incorrect_i2c_address(bus_number, incorrect_address)
    
    # Print the command output
    print(f"stdout:\n{stdout}")
    print(f"stderr:\n{stderr}")
    
    # Assert that the command failed
    assert returncode != 0, f"Unexpected success when reading from incorrect I2C address {hex(incorrect_address)}."
    assert "Failed" in stderr or "Error" in stderr, f"Expected error message not found when reading from incorrect I2C address {hex(incorrect_address)}."
    print("Error handling for incorrect I2C address verified successfully.")

if __name__ == "__main__":
    pytest.main([__file__])

