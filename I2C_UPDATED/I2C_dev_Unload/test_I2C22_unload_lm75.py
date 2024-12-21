import subprocess
import pytest


"This test case is to unload the lm75 module"

def unload_lm75_module():

    print("Attempting to unload the lm75 module...")
    result = subprocess.run(['sudo', 'modprobe', '-r', 'lm75'],capture_output=True, text=True)
    return result.returncode


def load_lm75():

    if 'lm75' not in subprocess.getoutput('lsmod'):
       print("lm75 module is not loaded. Loading it now...")
       subprocess.run(['sudo', 'modprobe', 'lm75'], check=True)


def test_unload_lm75_module():

    print("\nStarting test for unloading lm75 module...")
    returncode = unload_lm75_module()
    assert returncode == 0, "Failed to unload lm75 module."
    print("lm75 module unloaded successfully.")
    load_lm75()

if __name__ == "__main__":
    pytest.main([__file__])

