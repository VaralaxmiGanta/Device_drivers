import subprocess
import re
import pytest

""" This test case is to verify that whether the driver initializes the submission and completion queues"""


def run_command(command):
    try:
        output = subprocess.check_output(command, shell=True, text=True)
        return output
    except subprocess.CalledProcessError as e:
        pytest.fail(f"Error executing command: {e}")


# Function to check queue initialization
def get_queue_sizes(nvme_device="/dev/nvme0"):
    cmd = f"sudo nvme id-ctrl {nvme_device}"
    output = run_command(cmd)
    
    submission_match = re.search(r"sqes\s+:\s+0x(\w+)", output)
    completion_match = re.search(r"cqes\s+:\s+0x(\w+)", output)

    if submission_match and completion_match:
        sqes = int(submission_match.group(1), 16)
        cqes = int(completion_match.group(1), 16)
        return sqes, cqes
    else:
        pytest.fail("Could not find SQES or CQES information.")


# Pytest test to check queue initialization
def test_queue_initialization():

    sqes, cqes = get_queue_sizes("/dev/nvme0")
    
    assert sqes != 0, f"\nSubmission Queue Entry Size (SQES) is not initialized, found: {sqes}"
    assert cqes != 0, f"\nCompletion Queue Entry Size (CQES) is not initialized, found: {cqes}"

    print(f"Submission Queue Entry Size (SQES): {sqes}")
    print(f"Completion Queue Entry Size (CQES): {cqes}")
