import time
from QFramework.StorageAutomation import Storage
import json

storage = Storage()


def test_case_08():
    """Restart QEMU and verify devices are present."""
    print("started test case 08")
    with open(r"/Framework/resource.json", "r") as file:
        device = json.load(file)
    image = device["device"]

    storage.QemuStart()
    storage.add_device("ucbdisk1", image["image1"], "usb1")

    # Restart QEMU
    storage.QemuRestart()
    time.sleep(240)  # Wait for devices to be re-initialized

    Output = storage.list_device()

    # Remove the device after verification
    storage.remove_device("usb1")
    storage.QemuStop()

    # Assert that the device is listed after restart
    assert "QEMU USB HARDDRIVE" in Output, f"Expected 'QEMU USB HARDDRIVE' in output but got: {Output}"
