import time
from QFramework.StorageAutomation import Storage
import json

storage = Storage()


def test_case_07():
    """Attach multiple USB devices and list them."""
    print("start test case 07")
    with open(r"/home/vlab/PycharmProjects/Linux Automation/Framework/resource.json", "r") as file:
        device = json.load(file)
    images = device["device"]

    storage.QemuStart()
    for i, (key, image_path) in enumerate(images.items(), start=1):
        storage.add_device(f"ucbdisk{i}", image_path, f"usb{i}")

    Output = storage.list_device()

    for i in range(1, len(images) + 1):
        storage.remove_device(f"usb{i}")

    storage.QemuStop()

    # Assert that the expected string is in the output
    assert "QEMU USB HARDDRIVE" in Output, f"Expected 'QEMU USB HARDDRIVE' in output but got: {Output}"
