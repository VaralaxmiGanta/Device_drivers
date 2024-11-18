import time
import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))

from QFramework.StorageAutomation import Storage
import json

storage = Storage()


def test_case_01():
    print("started test case 01")
    with open(r"Tests/test_inputs/resource.json", "r") as file:
        device = json.load(file)
    image = device["device"]

    storage.QemuStart()
    storage.add_device("ucbdisk1", image["image1"], "usb1")
    Output = storage.list_device()
    storage.remove_device("usb1")
    storage.QemuStop()

    assert "QEMU USB HARDDRIVE" in Output, "Expected 'QEMU USB HARDDRIVE' in Output, but it was not found"
