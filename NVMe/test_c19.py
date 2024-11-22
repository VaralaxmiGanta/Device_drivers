
import subprocess
import re
import pytest
""" This Test case is to verify whether the pcie configuration space initialized successfully"""

def get_nvme_device_info():
    """Fetches PCI configuration space details for the NVMe device."""
    try:
        output = subprocess.check_output(["lspci", "-vvv"]).decode("utf-8")
        pattern = r"([0-9a-fA-F]{2}):([0-9a-fA-F]{2})\.([0-9])\s+Non-Volatile memory controller"
        
        matches = re.findall(pattern, output)
        
        if not matches:
            raise Exception("No NVMe device found.")
        
        nvme_info = []
        for match in matches:
            bus_no, device_no, func_no = match
            vendor_id = subprocess.check_output(f"setpci -s {bus_no}:{device_no}.{func_no} 0x00.w", shell=True).decode("utf-8").strip()
            device_id = subprocess.check_output(f"setpci -s {bus_no}:{device_no}.{func_no} 0x02.w", shell=True).decode("utf-8").strip()
            bar0 = subprocess.check_output(f"setpci -s {bus_no}:{device_no}.{func_no} 0x10.w", shell=True).decode("utf-8").strip()
            
            nvme_info.append({
                "bus": bus_no,
                "device": device_no,
                "function": func_no,
                "vendor_id": vendor_id,
                "device_id": device_id,
                "bar0": bar0
            })
        
        return nvme_info
    
    except subprocess.CalledProcessError as e:
        pytest.fail(f"Error occurred while accessing PCI configuration: {e}")
    except Exception as e:
        pytest.fail(str(e))


@pytest.fixture(scope="module")
def nvme_device_info():
    return get_nvme_device_info()


def test_nvme_device(nvme_device_info):
    for device in nvme_device_info:
        print(f"NVMe Device found - Bus: {device['bus']}, Device: {device['device']}, Function: {device['function']}")
        print(f"Vendor ID: {device['vendor_id']}, Device ID: {device['device_id']}")
        print(f"BAR0: {device['bar0']}")
