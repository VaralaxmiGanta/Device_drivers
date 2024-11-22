import subprocess
import re
import pytest

""" This Test case is to verify whether the pcie bus enumeration performed successfully"""
def check_nvme_device():
    try:
        output = subprocess.check_output(["lspci"]).decode("utf-8")
        pattern = r"([0-9a-fA-F]{2}):([0-9a-fA-F]{2})\.([0-9])\s+Non-Volatile memory controller"
        
        matches = re.findall(pattern, output)
        
        if matches:
            for match in matches:
                bus_no, device_no, func_no = match
                print(f"NVMe Device found - Bus: {bus_no}, Device: {device_no}, Function: {func_no}")
            return True
        else:
            print("No NVMe device found.")
            return False

    except subprocess.CalledProcessError as e:
        print(f"Error occurred: {e}")
        return False


def test_nvme_device_found():
    assert check_nvme_device(), "No NVMe device found on the PCI bus."

