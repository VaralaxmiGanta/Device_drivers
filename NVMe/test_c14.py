import json
import subprocess
import pytest

""" This test case is to verify the Bandwidth for different types of operations"""

# Function to run the FIO test and capture Bandwidth
def run_fio_test_bandwidth(test_name, rw_type, filename):
    command = [
        'fio',
        f'--name={test_name}',
        '--ioengine=libaio',
        f'--rw={rw_type}',
        '--bs=4k',
        '--numjobs=4',
        '--runtime=60',  # Run for 1 minute
        '--iodepth=32',
        '--direct=1',
        f'--filename={filename}',
        '--output-format=json'
    ]

    print(f"Running {test_name} on NVMe device...")
    result = subprocess.run(command, capture_output=True, text=True, check=True)
    output = json.loads(result.stdout)

    # Extract Bandwidth in MB/s
    bandwidth = 0
    if rw_type in ['randread', 'read']:
        bandwidth = output['jobs'][0].get('read', {}).get('bw', 0) / 1024  # Convert KB/s to MB/s
    elif rw_type in ['randwrite', 'write']:
        bandwidth = output['jobs'][0].get('write', {}).get('bw', 0) / 1024  # Convert KB/s to MB/s

    return bandwidth

@pytest.mark.parametrize("test_name, rw_type", [
    ("random-read-test", "randread"),
    ("random-write-test", "randwrite"),
    ("sequential-read-test", "read"),
    ("sequential-write-test", "write")
])

def test_fio_bandwidth(test_name, rw_type):
    filename = '/dev/nvme0n1'
    bandwidth = run_fio_test_bandwidth(test_name, rw_type, filename)

    # Assert that the bandwidth is above the expected threshold
    print(f"{test_name} - Bandwidth: {bandwidth} MB/s")
    assert bandwidth > 0, f"Bandwidth for {test_name} is below expected threshold. Actual: {bandwidth} MB/s"
