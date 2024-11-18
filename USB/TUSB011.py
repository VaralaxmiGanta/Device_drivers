import time
from QFramework.StorageAutomation import Storage
import json

storage = Storage()

def test_case_11():
    print("start test case 11")
    with open(r"/Framework/resource.json", "r") as file:
        device = json.load(file)
    image = device["device"]

    storage.QemuStart()
    storage.add_device("ucbdisk1", image["image1"], "usb1")
    storage.mount_device()

    storage.write_large_file("/mnt/usb/largefile")
    storage.read_large_file("/mnt/usb/largefile", "/tmp/")
    Output = storage.cheach_for_file("/tmp/largefile")
    storage.delete_file("/mnt/usb/largefile")

    storage.unmount_device()
    storage.remove_device("usb1")
    storage.QemuStop()

    # Assert that the large file is correctly found at /tmp/largefile
    assert "/tmp/largefile" == Output, f"Expected '/tmp/largefile', but got {Output}"
