import subprocess
import pytest

def is_module_loaded(module_name):
    """
    Check if the specified module is loaded.
    """
    result = subprocess.run(['lsmod'], capture_output=True, text=True)
    return module_name in result.stdout

def load_module(module_name):
    """
    Load the specified module.
    """
    print(f"Attempting to load the {module_name} module...")
    result = subprocess.run(['sudo', 'modprobe', module_name], capture_output=True, text=True)
    print(f"Command executed with return code: {result.returncode}")
    return result.returncode

def unload_module(module_name):
    """
    Unload the specified module.
    """
    print(f"Attempting to unload the {module_name} module...")
    result = subprocess.run(['sudo', 'modprobe', '-r', module_name], capture_output=True, text=True)
    print(f"Command executed with return code: {result.returncode}")
    return result.returncode

def test_load_and_unload_i2c_piix4_module():
    """
    Test the loading and unloading of the i2c-piix4 module.
    """
    module_name = 'i2c-piix4'
    
    print(f"\nStarting test for {module_name} module...")

    # Check if the module is loaded
    if not is_module_loaded(module_name):
        print(f"{module_name} module is not loaded. Loading it now...")
        returncode = load_module(module_name)
        assert returncode == 0, f"Failed to load {module_name} module."
        print(f"{module_name} module loaded successfully.")
    else:
        print(f"{module_name} module is already loaded.")

    # Unload the module
    returncode = unload_module(module_name)
    assert returncode == 0, f"Failed to unload {module_name} module."
    print(f"{module_name} module unloaded successfully.")

if __name__ == "__main__":
    pytest.main([__file__])

