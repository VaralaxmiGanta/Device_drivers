import subprocess
import os
import time
import threading
import pytest
from Inputs.common_inputs import Inputs


"This test case is to verify the module unload while in use"

def load_module(module_name):
    result = subprocess.run(['sudo', 'modprobe', module_name], capture_output=True, text=True)
    return result.returncode, result.stdout, result.stderr

def continuous_access(bus_number):
    def access_loop():
        while not stop_event.is_set():
            subprocess.run(['sudo', 'i2cdetect', '-y', str(bus_number)], capture_output=True, text=True)
            time.sleep(1)

    stop_event = threading.Event()
    thread = threading.Thread(target=access_loop)
    thread.start()
    return thread, stop_event

def unload_module(module_name):
    result = subprocess.run(['sudo', 'modprobe', '-r', module_name], capture_output=True, text=True)
    return result.returncode, result.stdout, result.stderr

def test_unload_module_in_use():

    module_name = 'i2c-dev'

    # Ensure the module is loaded
    print("\nLoading the module...")
    returncode, stdout, stderr = load_module(module_name)
    assert returncode == 0, f"Failed to load module: {stderr}"

    print("Using the module continuously...")
    thread, stop_event = continuous_access(Inputs.I2C_BUS)
    time.sleep(5)

    # Attempt to unload the module
    print("Attempting to unload the module while in use...")
    returncode, stdout, stderr = unload_module(module_name)
    stop_event.set()
    thread.join()
    print(f"stdout:\n{stdout}")
    print(f"stderr:\n{stderr}")

    assert returncode != 0, "Unexpected success when unloading the module while it is in use."
    assert "in use" in stderr, "Expected 'in use' error message not found when unloading the module."

    print("Module unloading while in use verified successfully.")

if __name__ == "__main__":
    pytest.main([__file__])

