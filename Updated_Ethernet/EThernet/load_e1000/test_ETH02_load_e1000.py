import subprocess


"This test case is to verify whether the e1000 module is loaded or not. If not the module will be loaded"


def test_load_e1000_module():
    print("\nStarting test for loading e1000 module...")

    # Check if the e1000 module is loaded, if not, load it
    if "e1000" not in subprocess.getoutput('lsmod'):
        print("e1000 module is not loaded. Loading it now...")
        subprocess.run(['sudo', 'modprobe', 'e1000'], check=True)
    
    # Verify the module is loaded
    assert "e1000" in subprocess.getoutput('lsmod'), "e1000 module not loaded."
    print("e1000 module already loaded successfully.")
    



if __name__ == "__main__":
    test_load_e1000_module()
