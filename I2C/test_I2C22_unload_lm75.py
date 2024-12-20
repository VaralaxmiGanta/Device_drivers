import subprocess
import pytest

def unload_lm75_module():
    print("Attempting to unload the lm75 module...")
    result = subprocess.run(['sudo', 'modprobe', '-r', 'lm75'],capture_output=True, text=True)

    print(f"Command executed with return code: {result.returncode}")
    return result.returncode

def test_unload_lm75_module():
    print("\nStarting test for unloading lm75 module...")
    returncode = unload_lm75_module()
    assert returncode == 0, "Failed to unload lm75 module."
    print("i2c-lm75 module unloaded successfully.")

if __name__ == "__main__":
    pytest.main([__file__])

