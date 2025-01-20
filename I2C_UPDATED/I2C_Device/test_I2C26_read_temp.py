import pytest
import os
"This test case is to read the value of temperature using temp1_input file in the hwmon directory "


def find_hwmon_device():

    hwmon_base_dir = "/sys/class/hwmon"
    for hwmon_dir in os.listdir(hwmon_base_dir):
        hwmon_path = os.path.join(hwmon_base_dir, hwmon_dir)
        if os.path.isdir(hwmon_path):
            # Check if the temperature file exists in this directory
            temp_file = os.path.join(hwmon_path, "temp1_input")
            if os.path.exists(temp_file):
                return hwmon_dir, temp_file
    return None, None

def test_find_hwmon_device():

    hwmon_dir, temp_file = find_hwmon_device()
    # Assert that the hwmon device is found and not None
    assert hwmon_dir is not None, "No hwmon device found!"
    assert hwmon_dir.startswith('hwmon'), f"Expected hwmon device, got {hwmon_dir}"

    # Read and print the temperature if the device is found
    if temp_file:
        with open(temp_file, 'r') as f:
            temp = f.read().strip()
            print(f"Temperature reading from {temp_file}: {temp} (raw value)")


