import time
from QFramework.StorageAutomation import Storage
import json

storage = Storage()

def test_case_13():
    """Measure IO performance on the mounted USB device."""
    print("start test case 13")
    with open(r"/Framework/resource.json", "r") as file:
        device = json.load(file)
    image = device["device"]

    storage.QemuStart()
    storage.add_device("ucbdisk1", image["image1"], "usb1")
    storage.mount_device()

    Output = storage.io_measurement("/mnt/usb/")

    storage.unmount_device()
    storage.remove_device("usb1")
    storage.QemuStop()

    # Assert that the output contains "requests"
    assert "requests" in Output, f"Expected 'requests' in output, but got: {Output}"

