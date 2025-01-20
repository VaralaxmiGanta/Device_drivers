import subprocess
import os

"This test case is to load the lm75 module"


def test_load_lm75_module_and_devices():
    print("\nStarting test for loading lm75  module...")

    # Check if the i2c-dev module is loaded, if not, load it
    if 'lm75' not in subprocess.getoutput('lsmod'):
        print("lm75 module is not loaded. Loading it now...")
        subprocess.run(['sudo', 'modprobe', 'lm75'], check=True)
    
    # Verify the module is loaded
    assert 'lm75' in subprocess.getoutput('lsmod'), "lm75 module not loaded."
    print("lm75 module already loaded successfully.")


    expected_devices = ["/dev/i2c-0", "/sys/bus/i2c/devices/0-0048"]

    for device in expected_devices:
         print(f"Checking for I2C device: {device}")
         assert os.path.exists(device), f"{device} does not exist."
         print(f"{device} exists.")

    # # Check if LM75 devices exist
    # for device in ["/dev/i2c-0"]:
    #     print("I2C Devices Found: ",device)
    #     assert os.path.exists(device), f"{device} does not exist."


# Run the test
if __name__ == "__main__":
    test_load_lm75_module_and_devices()


