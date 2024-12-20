import subprocess
import pytest

def scan_i2c_bus(bus_number):
    print(f"Scanning I2C bus {bus_number} for devices...")
    # Run the command to scan I2C bus
    result = subprocess.run(['sudo', 'i2cdetect', '-y', str(bus_number)], capture_output=True, text=True)
    return result.returncode, result.stdout

def test_scan_i2c_bus():
    bus_number = 0  # Change to the appropriate bus number if needed
    print("\nStarting test for scanning I2C bus for devices...")
    # Scan the I2C bus and capture the result
    returncode, stdout = scan_i2c_bus(bus_number)
    
    # Print the command output
    print(f"Output:\n{stdout}")
    
    # Assert that the command executed successfully
    assert returncode == 0, f"Failed to scan I2C bus {bus_number}."
    assert "0:" in stdout, f"No devices found on I2C bus {bus_number}."
    print("I2C bus scanned successfully and devices found.")

if __name__ == "__main__":
    pytest.main([__file__])

