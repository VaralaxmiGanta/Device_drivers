import json
import subprocess
import pytest

"""This Test case is to verify that whether sequential write operations on an nvme device performed successfully."""

def run_fio_test():
    command = [
        'fio',
        '--name=sequential-write-test',
        '--ioengine=libaio',
        '--rw=write',  # sequential write operation
        '--bs=4k',
        '--numjobs=1',
        '--runtime=10',
        '--iodepth=32',
        '--direct=1',
        '--filename=/mnt/nvme0/test_seq_write',
        '--size=1G',
        '--output-format=json'
    ]
    print("Running sequential write tests on test file")

    result = subprocess.run(command, capture_output=True, text=True, check=True)
    output = json.loads(result.stdout)

    job_runtime_ms = output['jobs'][0]['job_runtime']  # Job runtime in milliseconds
    job_runtime_s = job_runtime_ms / 1000  # Convert to seconds
    total_ios = output['jobs'][0]['write']['total_ios']  # Total I/O operations for write
    iops = output['jobs'][0]['write']['iops']  # IOPS for write

    return job_runtime_s, total_ios, iops

def test_seqential_write_operation():

    job_runtime_s, total_ios, iops = run_fio_test()

    # Assert that the test completed with a positive job runtime, I/O operations, and IOPS
    assert job_runtime_s > 0, "Job runtime should be positive"
    assert total_ios > 0, "Total I/O operations should be greater than 0"
    assert iops > 0, "IOPS should be greater than 0"

    print(f"Job Runtime: {job_runtime_s:.2f} seconds")
    print(f"Total I/O Operations: {total_ios}")
    print(f"I/O Operations Per Second (IOPS): {iops:.2f}")

if __name__ == "__main__":
    pytest.main()
