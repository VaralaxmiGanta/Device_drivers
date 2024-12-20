import subprocess
import pytest

def unload_i2c_dev_module():
    print("Attempting to unload the i2c-dev module...")
    result = subprocess.run(['sudo', 'modprobe', '-r', 'i2c-dev'], capture_output=True, text=True)
    print(f"Command executed with return code: {result.returncode}")
    return result.returncode

def test_unload_i2c_dev_module():
    print("\nStarting test for unloading i2c-dev module...")
    returncode = unload_i2c_dev_module()
    assert returncode == 0, "Failed to unload i2c-dev module."
    print("i2c-dev module unloaded successfully.")

if __name__ == "__main__":
    pytest.main([__file__])

