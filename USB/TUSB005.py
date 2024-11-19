import time
from QFramework.StorageAutomation import Storage
import json

storage = Storage()


def test_case_05():
    """Reading a file from the mounted USB device."""
    print("start test case 05")
    with open(r"/Framework/resource.json", "r") as file:
        device = json.load(file)
    image = device["device"]

    storage.QemuStart()
    storage.add_device("ucbdisk1", image["image1"], "usb1")
    storage.mount_device()
    storage.create_file("/mnt/usb/testfile.txt")
    storage.file_permissions("777", "/mnt/usb/testfile.txt")
    storage.write_file("/mnt/usb/testfile.txt", "This is Soctronics")

    # Attempt to read the file
    Output = storage.read_file("/mnt/usb/testfile.txt")

    storage.unmount_device()
    storage.remove_device("usb1")
    storage.QemuStop()

    print("output: ", Output)

    # Assert that the expected content is in the output
    assert "This is Soctronics" in Output, "Expected content not found in the file. The file content was: " + Output
