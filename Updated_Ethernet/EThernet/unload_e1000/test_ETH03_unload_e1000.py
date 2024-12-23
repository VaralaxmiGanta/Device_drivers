import subprocess
import pytest


"This test case is to unload_e1000 the e1000 module"

def unload_e1000_module():

    print("Attempting to unload_e1000 the e1000 module...")
    result = subprocess.run(['sudo', 'modprobe', '-r', 'e1000'],capture_output=True, text=True)
    return result.returncode


def load_e1000():

    if 'e1000' not in subprocess.getoutput('lsmod'):
       print("e1000 module is not loaded. Loading it now...")
       subprocess.run(['sudo', 'modprobe', 'e1000'], check=True)


def test_unload_e1000_module():

    print("\nStarting test for unloading e1000 module...")
    returncode = unload_e1000_module()
    assert returncode == 0, "Failed to unload_e1000 e1000 module."
    print("e1000 module unloaded successfully.")
    load_e1000()

if __name__ == "__main__":
    pytest.main([__file__])
