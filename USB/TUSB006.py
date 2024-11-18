import time
from QFramework.StorageAutomation import Storage
import json

storage = Storage()


def test_case_06():
    """Remove and re-add the USB device in QEMU monitor."""
    print("start test case 06")
    with open(r"/Framework/resource.json", "r") as file:
        device = json.load(file)
    image = device["device"]

    storage.QemuStart()
    storage.add_device("ucbdisk1", image["image1"], "usb1")
    storage.remove_device("usb1")
    storage.add_device("ucbdisk1", image["image1"], "usb1")

    Output = storage.list_device()

    storage.remove_device("usb1")
    storage.QemuStop()

    # Assert that the expected string is in the output
    assert "QEMU USB HARDDRIVE" in Output, f"Expected 'QEMU USB HARDDRIVE' in output but got: {Output}"
