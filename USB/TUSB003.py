import time
from QFramework.StorageAutomation import Storage
import json

storage = Storage()


def test_case_03():
    print("start test case 03")
    with open(r"/Framework/resource.json", "r") as file:
        device = json.load(file)
    image = device["device"]

    storage.QemuStart()
    storage.add_device("ucbdisk1", image["image1"], "usb1")
    storage.mount_device()
    storage.unmount_device()
    Output = storage.list_block_device()
    storage.remove_device("usb1")
    storage.QemuStop()

    # Assert that neither "sda" nor "/mnt/usb" is in the output
    assert "sda" not in Output, "Expected 'sda' not to be in Output, but it was found"
    assert "/mnt/usb" not in Output, "Expected '/mnt/usb' not to be in Output, but it was found"
