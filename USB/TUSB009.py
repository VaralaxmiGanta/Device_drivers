import time
from QFramework.StorageAutomation import Storage
import json

storage = Storage()

def test_case_09():
    """Create a new file on the mounted USB device."""
    print("start test case 9")
    with open(r"/Framework/resource.json", "r") as file:
        device = json.load(file)
    image = device["device"]

    storage.QemuStart()
    storage.add_device("ucbdisk1", image["image1"], "usb1")
    storage.mount_device()

    # Create a new file on the USB device
    Output = storage.create_file("/mnt/usb/testfile2.txt")

    storage.unmount_device()
    storage.remove_device("usb1")
    storage.QemuStop()

    # Assert that the file creation was successful (Output should be 0)
    assert Output == 0, f"Expected Output to be 0, but got {Output}"
