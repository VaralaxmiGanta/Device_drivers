import time
from QFramework.StorageAutomation import Storage
import json

storage = Storage()

def test_case_10():
    print("start test case 10")
    with open(r"/Framework/resource.json", "r") as file:
        device = json.load(file)
    image = device["device"]

    storage.QemuStart()
    storage.add_device("ucbdisk1", image["image1"], "usb1")
    storage.mount_device()

    path = "/mnt/usb/largefile"
    storage.write_large_file(path)
    Output = storage.cheach_for_file(path)  # Assuming this method checks for the file
    storage.delete_file(path)

    storage.unmount_device()
    storage.remove_device("usb1")
    storage.QemuStop()

    # Assert that the file path matches the expected output
    assert path == Output, f"Expected file at {path}, but got {Output}"
