import subprocess
import pytest
""" This test case is to verify that whether the nvme device and driver supports different types of filesystems"""

@pytest.mark.parametrize("filesystem, mount_point", [
    ("ext4", "/mnt/ext4"),
    ("xfs", "/mnt/xfs"),
    ("btrfs", "/mnt/btrfs"),
    ("f2fs", "/mnt/f2fs")
])
def test_nvme_driver_filesystem_support(filesystem, mount_point):
    try:
        # Ensure the mount point directories exist
        subprocess.run(["sudo", "mkdir", "-p", mount_point], check=True)
        print(f"Created mount point: {mount_point}")
    except subprocess.CalledProcessError as e:
        pytest.fail(f"Failed to create mount point {mount_point}: {e}")
        return

    try:
        # Step 1: Format the device with the given file system
        subprocess.run(["sudo", "mkfs." + filesystem, "/dev/nvme0n1"], check=True)
        print(f"Filesystem {filesystem} created successfully.")
    except subprocess.CalledProcessError as e:
        pytest.fail(f"Failed to format {filesystem}: {e}")
        return

    try:
        # Step 2: Mount the file system
        subprocess.run(["sudo", "mount", "/dev/nvme0n1", mount_point], check=True)
        print(f"Mounted {filesystem} at {mount_point}.")
    except subprocess.CalledProcessError as e:
        pytest.fail(f"Failed to mount {filesystem} at {mount_point}: {e}")
        return

    try:
        # Step 3: Perform basic file operations (Create, write, read, delete)
        test_file = mount_point + "/testfile"
        subprocess.run(["touch", test_file], check=True)
        subprocess.run(["echo", "Test data", ">", test_file], check=True)
        subprocess.run(["cat", test_file], check=True)
        subprocess.run(["rm", test_file], check=True)
    except subprocess.CalledProcessError as e:
        pytest.fail(f"File operations failed for {filesystem}: {e}")

    try:
        # Step 4: Check the system logs for errors
        result = subprocess.run(["dmesg", "|", "grep", "nvme"], capture_output=True, text=True)
        assert "error" not in result.stdout.lower(), f"Error found in dmesg logs for {filesystem}"
    except subprocess.CalledProcessError as e:
        pytest.fail(f"Failed to check dmesg logs: {e}")

    try:
        # Step 5: Unmount the file system
        subprocess.run(["sudo", "umount", mount_point], check=True)
        print(f"Unmounted {filesystem} from {mount_point}.")
    except subprocess.CalledProcessError as e:
        pytest.fail(f"Failed to unmount {filesystem} from {mount_point}: {e}")
