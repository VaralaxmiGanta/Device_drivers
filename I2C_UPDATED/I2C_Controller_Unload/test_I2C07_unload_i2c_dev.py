import subprocess
import pytest

"This test case is to unload the i2c_dev module"

def unload_i2c_dev_module():

    print("Attempting to unload the i2c-dev module...")
    result = subprocess.run(['sudo', 'modprobe', '-r', 'i2c-dev'], capture_output=True, text=True)
    return result.returncode

def load_i2c_dev():

    if 'i2c_dev' not in subprocess.getoutput('lsmod'):
       print("i2c-dev module is not loaded. Loading it now...")
       subprocess.run(['sudo', 'modprobe', 'i2c-dev'], check=True)

def test_unload_i2c_dev_module():

    load_i2c_dev()
    print("\nStarting test for unloading i2c-dev module...")
    returncode = unload_i2c_dev_module()
    assert returncode == 0, "Failed to unload i2c-dev module."
    print("i2c-dev module unloaded successfully.")
    load_i2c_dev()

if __name__ == "__main__":
    pytest.main([__file__])

