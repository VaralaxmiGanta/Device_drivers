import subprocess
import pytest

"This test case is to verify the negative scenario of scanning non-existent bus number for I2C devices"

def scan_non_existent_i2c_bus(bus_number):

    print(f"Scanning non-existent I2C bus {bus_number} for devices...")
    result = subprocess.run(['sudo', 'i2cdetect', '-y', str(bus_number)], capture_output=True, text=True)
    return result.returncode, result.stdout, result.stderr

def test_non_existent_i2c_bus():

    bus_number = 10  # Use a bus number that doesn't exist
    print("\nStarting test for scanning non-existent I2C bus...")
    returncode, stdout, stderr = scan_non_existent_i2c_bus(bus_number)

    print(f"stdout:\n{stdout}")
    print(f"stderr:\n{stderr}")
    
    assert returncode != 0, f"Unexpected success when scanning non-existent I2C bus {bus_number}."
    assert "No such file or directory" in stderr, f"Expected error message not found when scanning non-existent I2C bus {bus_number}."
    print("Error handling for non-existent I2C bus verified successfully.")

if __name__ == "__main__":
    pytest.main([__file__])

