import subprocess
import pytest

"This test case is to unload the i2c_piix4 module"

def unload_i2c_piix4_module():

    print("Attempting to unload the i2c-piix4 module...")
    result = subprocess.run(['sudo', 'modprobe', '-r', 'i2c-piix4'], capture_output=True, text=True)
    return result.returncode

def load_i2c_piix4():

    if 'i2c_piix4' not in subprocess.getoutput('lsmod'):
       print("i2c-piix4 module is not loaded. Loading it now...")
       subprocess.run(['sudo', 'modprobe', 'i2c-piix4'], check=True)

def test_unload_i2c_dev_module():

    print("\nStarting test for unloading i2c-piix4 module...")
    returncode = unload_i2c_piix4_module()
    assert returncode == 0, "Failed to unload i2c-piix4 module."
    print("i2c-piix4 module unloaded successfully.")
    load_i2c_piix4()

if __name__ == "__main__":
    pytest.main([__file__])

