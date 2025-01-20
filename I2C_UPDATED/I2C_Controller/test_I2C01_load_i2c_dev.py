import subprocess
import os

"This test case is to verify whether the i2c_dev module is loaded or not. If not the module will be loaded"


def test_load_i2c_dev_module_and_devices():
    print("\nStarting test for loading i2c-dev module...")

    # Check if the i2c-dev module is loaded, if not, load it
    if 'i2c_dev' not in subprocess.getoutput('lsmod'):
        print("i2c-dev module is not loaded. Loading it now...")
        subprocess.run(['sudo', 'modprobe', 'i2c-dev'], check=True)
    
    # Verify the module is loaded
    assert 'i2c_dev' in subprocess.getoutput('lsmod'), "i2c-dev module not loaded."
    print("i2c-dev module already loaded successfully.")
    
    # Check if I2C devices exist
    for device in ["/dev/i2c-0"]:
        print("I2C Devices Found: ",device)
        assert os.path.exists(device), f"{device} does not exist."


if __name__ == "__main__":
    test_load_i2c_dev_module_and_devices()

