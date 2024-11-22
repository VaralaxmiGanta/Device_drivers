import subprocess
import pytest

"""This Test case is to verify that whether the driver creates namespace for an nvme device successfully  """
def list_nvme_namespaces(nvme_device):
    try:
        result = subprocess.run(['sudo', 'nvme', 'list-ns', nvme_device], capture_output=True, text=True, check=True)
        print("Namespaces for NVMe device:\n")
        print(result.stdout)
        return result.stdout
    except subprocess.CalledProcessError as e:
        print(f"Error listing namespaces: {e}")
        return None


def test_list_nvme_namespaces():
    nvme_device = '/dev/nvme0'  # Change if necessary
    namespaces_output = list_nvme_namespaces(nvme_device)

    assert namespaces_output is not None, "Error: No output returned from 'list-ns' command"


if __name__ == "__main__":
    test_list_nvme_namespaces()
