import os
import subprocess
import pytest

"""This Test case is to verify data integrity whether the Data written to the Nvme device matches the read data """

device = '/dev/nvme0n1'
mount_point = '/mnt/nvme0'
file_path = os.path.join(mount_point, 'test_file06.txt')
file_content = "Test data for verification."

# Function to format the device as ext4
def format_device():
    print(f"\nFormatting {device} as ext4...")
    subprocess.run(['sudo', 'mkfs.ext4', '-F', device], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)


# Function to mount the device
def mount_device():
    print(f"\nMounting {device} to {mount_point}...")
    os.makedirs(mount_point, exist_ok=True)
    subprocess.run(['sudo', 'mount', device, mount_point], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)


# Function to write a file to the mounted device
def write_file():
    try:
        with open(file_path, 'w') as f:
            f.write(file_content)
        return os.path.exists(file_path)
    except PermissionError:
        print(f"PermissionError: Unable to write to {file_path}. Check permissions.")
        return False


# Function to read the file from the mounted device
def read_file():
    try:
        with open(file_path, 'r') as f:
            content = f.read()
        return content
    except FileNotFoundError:
        print(f"FileNotFoundError: Unable to find {file_path}. Ensure write operation was successful.")
        return None


# Function to unmount the device
def unmount_device():
    print(f"\nUnmounting {mount_point}...")
    subprocess.run(['sudo', 'umount', mount_point], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)


# pytest fixture to set up and tear down the mount environment
@pytest.fixture(scope="module", autouse=True)
def setup_and_teardown():
    format_device()
    mount_device()
    yield
    unmount_device()

# Test function for write operation
def test_write_file():
    assert write_file(), "Write operation failed: File was not created."


# Test function for read operation and data integrity
def test_read_file():
    content = read_file()
    assert content == file_content, f"Read operation failed: Expected '{file_content}', got '{content}'"


# Test function for data integrity verification
def test_data_integrity():
    write_file()
    read_data = read_file()

    # Assert that the written and read data match
    assert read_data == file_content, f"Data integrity check failed: Expected '{file_content}', got '{read_data}'"
    print("Written data matches the read data")
