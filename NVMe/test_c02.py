import subprocess
import pytest

"""This Test case is to check nvme device listing using nvme list command provided by package nvme-cli and also to check the nvme controller information """


def list_nvme_devices():
    try:
        result = subprocess.run(['sudo', 'nvme', 'list'], capture_output=True, text=True, check=True)
        return result.stdout
    except subprocess.CalledProcessError as e:
        return f"Error listing NVMe devices: {e}"


def identify_nvme_controller(device):
    try:
        result = subprocess.run(['sudo', 'nvme', 'id-ctrl', device], capture_output=True, text=True, check=True)
        return result.stdout
    except subprocess.CalledProcessError as e:
        return f"Error sending Identify Controller command: {e}"


# Test case to verify that the NVMe devices are listed
def test_list_nvme_devices():
    output = list_nvme_devices()
    print(output)
    assert "nvme0n1" in output, f"Expected to find NVMe device 'nvme0n1', but got: {output}"


# Test case to verify that the 'nvme id-ctrl' command works and gives the controller details for  specified device
def test_identify_nvme_controller():
    device = "/dev/nvme0n1"
    output = identify_nvme_controller(device)
    print(output)
    # Check if the Identify Controller output contains expected information
    assert "Identify Controller" in output, f"Expected to find controller info for {device}, but got: {output}"

if __name__ == "__main__":
    pytest.main()
