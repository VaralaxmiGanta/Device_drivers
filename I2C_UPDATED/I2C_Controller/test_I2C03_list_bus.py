
import pytest
import glob

"This test case is to verify whether there are i2c busses. if yes the busses device files will be printed"

def list_i2c_buses():
    print("Listing available I2C buses...")
    i2c_buses = glob.glob('/dev/i2c-*')
    if i2c_buses:
        print(f"Found I2C buses: {i2c_buses}")
        return 0, "\n".join(i2c_buses)
    else:
        return 1, ""

def test_list_i2c_buses():
    print("\nStarting test for listing available I2C buses...")
    returncode, stdout = list_i2c_buses()
    assert returncode == 0, "Failed to list I2C buses."
    assert '/dev/i2c-' in stdout, "No I2C buses found."
    print("Available I2C buses listed successfully.")

if __name__ == "__main__":
    pytest.main([__file__])

