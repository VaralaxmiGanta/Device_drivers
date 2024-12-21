import subprocess
import os

"This test case is to verify whether the i2c_piix4 module is loaded or not. If not the module will be loaded"


def test_load_i2c_piix4_module():
    print("\nStarting test for loading i2c-piix4 module...")

    # Check if the i2c-piix4 module is loaded, if not, load it
    if 'i2c_piix4' not in subprocess.getoutput('lsmod'):
        print("i2c-piix4 module is not loaded. Loading it now...")
        subprocess.run(['sudo', 'modprobe', 'i2c-piix4'], check=True)
    
    # Verify the module is loaded
    assert 'i2c_piix4' in subprocess.getoutput('lsmod'), "i2c-piix4 module not loaded."
    print("i2c-piix4 module already loaded successfully.")


if __name__ == "__main__":
    test_load_i2c_dev_module()

