import json
import subprocess
import pytest

"""This Test case is to verify that whether random read operations on an nvme device performed successfully."""
def run_fio_test():
    command = [
        'fio', 
        '--name=random-read-test', 
        '--ioengine=libaio', 
        '--rw=randread', #Random read operation
        '--bs=4k', 
        '--numjobs=1', 
        '--runtime=10', 
        '--iodepth=32', 
        '--direct=1', 
        '--filename=/dev/nvme0n1', 
        '--output-format=json'
    ]
    print("Running random read tests on NVMe device")
    
    result = subprocess.run(command, capture_output=True, text=True, check=True)
    output = json.loads(result.stdout)
    
    # Extract job runtime, total I/O operations, and IOPS
    job_runtime_ms = output['jobs'][0]['job_runtime']  # Job runtime in milliseconds
    job_runtime_s = job_runtime_ms / 1000  # Convert to seconds
    total_ios = output['jobs'][0]['read']['total_ios']  # Total I/O operations
    iops = output['jobs'][0]['read']['iops']  # IOPS

    return job_runtime_s, total_ios, iops


@pytest.fixture(scope="module", autouse=True)
def fio_test_setup():
    print("\nStarting Fio random read test...\n")
    yield run_fio_test()
    print("\nFio random read test completed.\n")


def test_random_read_operation(fio_test_setup):

    job_runtime_s, total_ios, iops = fio_test_setup

    assert total_ios > 0, "Total I/O operations should be greater than 0"
    assert iops > 0, "IOPS should be greater than 0"
    assert job_runtime_s > 0, "Job runtime should be greater than 0 seconds"
    
    print(f"Job Runtime: {job_runtime_s:.2f} seconds")
    print(f"Total I/O Operations: {total_ios}")
    print(f"I/O Operations Per Second (IOPS): {iops:.2f}")
