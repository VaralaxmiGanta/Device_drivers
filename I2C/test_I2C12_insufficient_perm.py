import subprocess
import os
import pytest

def change_permissions_with_sudo(device, permissions):
    result = subprocess.run(['sudo', 'chmod', permissions, device], capture_output=True, text=True)
    return result.returncode, result.stdout, result.stderr

def read_i2c_device(bus_number, address):
    print(f"Attempting to read from I2C address {address} on bus {bus_number} without sufficient permissions...")
    result = subprocess.run(['i2cget', '-y', str(bus_number), str(address)], capture_output=True, text=True)
    return result.returncode, result.stdout, result.stderr

def check_file_access(file_path, mode):
    try:
        with open(file_path, mode) as f:
            pass
        return True
    except IOError as e:
        return False

def test_insufficient_permissions():
    bus_number = 0  # Use the appropriate bus number
    device = '/dev/i2c-0'  # Device file for I2C bus
    device_address = 0x50  # Change to the correct address

    # Check if the device file exists
    if not os.path.exists(device):
        pytest.fail(f"Device file {device} does not exist")

    # Change permissions to make the device inaccessible
    print("\nChanging device permissions to 000...")
    returncode, stdout, stderr = change_permissions_with_sudo(device, '000')
    assert returncode == 0, f"Failed to change permissions: {stderr}"

    # Verify permissions
    print("\nVerifying permissions...")
    assert not check_file_access(device, 'r'), "File is still readable after changing permissions."
    assert not check_file_access(device, 'w'), "File is still writable after changing permissions."

    # Attempt to read from the I2C device
    read_returncode, read_stdout, read_stderr = read_i2c_device(bus_number, device_address)
    print(f"Read stdout:\n{read_stdout}")
    print(f"Read stderr:\n{read_stderr}")
    assert read_returncode != 0, f"Unexpected success when reading from I2C device at address {hex(device_address)} with insufficient permissions."
    assert "Permission denied" in read_stderr or "Device or resource busy" in read_stderr, \
        "Expected 'Permission denied' or 'Device or resource busy' error not found in read operation."

    # Restore permissions
    print("\nRestoring device permissions to 666...")
    returncode, stdout, stderr = change_permissions_with_sudo(device, '666')
    assert returncode == 0, f"Failed to restore permissions: {stderr}"
    print("Permissions test completed successfully.")

if __name__ == "__main__":
    pytest.main([__file__])

