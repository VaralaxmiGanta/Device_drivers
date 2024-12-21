import subprocess
import pytest

"This test case is to verify the devices on the bus number 0 if there are devices the devices addresses will be printed"


def scan_i2c_bus(bus_number):

    print(f"Scanning I2C bus {bus_number} for devices...")
    result = subprocess.run(['sudo', 'i2cdetect', '-y', str(bus_number)], capture_output=True, text=True)
    return result.returncode, result.stdout

def test_scan_i2c_bus():

    bus_number = 0

    print("\nStarting test for scanning I2C bus for devices...")
    returnee, stdout = scan_i2c_bus(bus_number)
    print(f"Output:\n{stdout}")
    
    assert returnee == 0, f"Failed to scan I2C bus {bus_number}."
    assert "0:" in stdout, f"No devices found on I2C bus {bus_number}."
    print("I2C bus scanned successfully and devices found.")

if __name__ == "__main__":
    pytest.main([__file__])

