import subprocess
import os

def test_load_i2c_piix4_module_and_devices():
    print("\nStarting test for loading i2c-piix4 module...")

    # Check if the i2c-dev module is loaded, if not, load it
    if 'i2c_piix4' not in subprocess.getoutput('lsmod'):
        print("i2c-piix4 module is not loaded. Loading it now...")
        subprocess.run(['sudo', 'modprobe', 'i2c-piix4'], check=True)
    
    # Verify the module is loaded
    assert 'i2c_piix4' in subprocess.getoutput('lsmod'), "i2c-piix4 module not loaded."
    print("i2c-piix4 module already loaded successfully.")
    
    # Check if I2C devices exist
    for device in ["/dev/i2c-0"]:
        print("I2C Devices Found: ",device)
        assert os.path.exists(device), f"{device} does not exist."


# Run the test
if __name__ == "__main__":
    test_load_i2c_dev_module_and_devices()

