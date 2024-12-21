import os
import stat
import pytest
import glob

"This test case is to verify the permissions on I2C device files for owner(root) and group members(I2C) and not for others"

def check_i2c_permissions():

    print("Checking permissions on I2C device files...")
    # List I2C device files
    i2c_files = glob.glob('/dev/i2c-*')
    if not i2c_files:
        return False, "No I2C device files found."
    
    for i2c_file in i2c_files:
        # Check the permissions
        st = os.stat(i2c_file)
        permissions = stat.filemode(st.st_mode)
        print(f"{i2c_file}: {permissions}")
        # Ensure the device has the appropriate permissions (rw for root and group i2c)
        if not (permissions == 'crw-rw----'):
            return False, f"Incorrect permissions for {i2c_file}: {permissions}"

    return True, "Permissions are correct for all I2C device files."

def test_check_i2c_permissions():

    print("\nStarting test for checking I2C device file permissions...")
    # Check permissions on I2C device files
    result, message = check_i2c_permissions()
    
    # Assert the permissions are correct
    assert result, message
    print("Permissions check passed for all I2C device files.")

if __name__ == "__main__":
    pytest.main([__file__])
