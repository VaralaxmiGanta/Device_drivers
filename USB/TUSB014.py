import time

from QFramework.StorageAutomation import Storage
import json

storage = Storage()

def test_case_14():
    """trying to read a file without premittons: security test"""
    print("start test case 14")
    with open(r"/Framework/resource.json", "r") as file:
        device = json.load(file)
    image = device["device"]

    storage.QemuStart()
    storage.add_device("ucbdisk1", image["image1"], "usb1")
    storage.mount_device()
    storage.create_file("/mnt/usb/testfile.txt")
    storage.file_permissions("a-w", "/mnt/usb/testfile.txt")
    storage.write_file("/mnt/usb/testfile.txt", "Hi this is Abhishek")
    # Attempt to read a file
    Output = storage.read_file("/mnt/usb/testfile.txt")
    storage.unmount_device()
    storage.remove_device("usb1")
    storage.QemuStop()
    print("output: ", Output)
    return "NOT OK" if "Hi this is Abhishek" in Output else "OK"