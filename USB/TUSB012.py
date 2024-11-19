import time
from QFramework.StorageAutomation import Storage
import json

storage = Storage()

def test_case_12():
    """Write several files sequentially to the USB device."""
    print("start test case 12")
    with open(r"/Framework/resource.json", "r") as file:
        device = json.load(file)
    image = device["device"]

    storage.QemuStart()
    storage.add_device("ucbdisk1", image["image1"], "usb1")
    storage.mount_device()

    for i in range(5):  # Adjust range for the number of files
        storage.write_large_file(f"/mnt/usb/largefile{i}")
        storage.read_large_file(f"/mnt/usb/largefile{i}", "/tmp/")
        Output = storage.cheach_for_file(f"/tmp/largefile{i}")
        storage.delete_file(f"/mnt/usb/largefile{i}")
        # Assert that the file was successfully read and is present in /tmp
        assert f"/tmp/largefile{i}" == Output, f"File /tmp/largefile{i} not found. Expected output: /tmp/largefile{i}, but got: {Output}"

    for i in range(5):
        storage.delete_file(f"/mnt/usb/largefile{i}")

    storage.unmount_device()
    storage.remove_device("usb1")
    storage.QemuStop()
