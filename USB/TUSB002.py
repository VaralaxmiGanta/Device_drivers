import time
from QFramework.StorageAutomation import Storage
import json

storage = Storage()


def test_case_02():
    print("start test case 02")
    with open(r"/Framework/resource.json", "r") as file:
        device = json.load(file)
    image = device["device"]

    storage.QemuStart()
    storage.add_device("ucbdisk1", image["image1"], "usb1")
    storage.mount_device()
    Output = storage.list_block_device()
    storage.unmount_device()
    storage.remove_device("usb1")
    storage.QemuStop()

    assert "sda" in Output, "Expected 'sda' in Output, but it was not found"
    assert "/mnt/usb" in Output, "Expected '/mnt/usb' in Output, but it was not found"
