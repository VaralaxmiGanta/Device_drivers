import subprocess
import re
import pytest

""" This test case is to measure the Latency for read and write operations"""

# Define expected latency ranges for read and write operations
EXPECTED_READ_LATENCY = {
    'min': (3, 10),    # in ms
    'avg': (3, 40),   # in ms
    'max': (3, 100),  # in ms
}

EXPECTED_WRITE_LATENCY = {
    'min': (50, 160),  # Minimum latency range in ms
    'avg': (50, 160), # Average latency range in ms
    'max': (50, 200), # Maximum latency range in ms
}


def run_ioping(device, num_operations=5, test_type="read"):

    if test_type == "read":
        command = f"sudo ioping -c {num_operations} {device}"
    elif test_type == "write":
        command = f"sudo ioping -WWW -c {num_operations} {device}"
    else:
        print("Invalid test type. Use 'read' or 'write'.")
        return None

    try:
        result = subprocess.run(command, capture_output=True, text=True, check=True, shell=True)
        print(f"Raw ioping {test_type} output:")
        print(result.stdout)

        stats_pattern = r"min/avg/max/mdev = ([\d.]+) ms / ([\d.]+) ms / ([\d.]+) ms / ([\d.]+) (ms|us)"
        match = re.search(stats_pattern, result.stdout)
        if match:
            min_latency_ms = float(match.group(1))
            avg_latency_ms = float(match.group(2))
            max_latency_ms = float(match.group(3))
            mdev_latency_ms = float(match.group(4))
            print(f"Filtered Latency Stats for {test_type.capitalize()}:")
            print(f"Min Latency: {min_latency_ms} ms")
            print(f"Avg Latency: {avg_latency_ms} ms")
            print(f"Max Latency: {max_latency_ms} ms")
            print(f"Latency Mdev: {mdev_latency_ms} ms")
            return {
                'min': min_latency_ms,
                'avg': avg_latency_ms,
                'max': max_latency_ms,
                'mdev': mdev_latency_ms
            }
        else:
            print("Could not extract latency values from ioping output.")
            return None
    except subprocess.CalledProcessError as e:
        print(f"Error running ioping: {e}")
        return None

@pytest.mark.parametrize("test_type,expected_latency", [
    ("read", EXPECTED_READ_LATENCY),
    ("write", EXPECTED_WRITE_LATENCY)
])
def test_latency(test_type, expected_latency):

    device = '/dev/nvme0n1'
    latency_stats = run_ioping(device, num_operations=5, test_type=test_type)

    assert latency_stats is not None, "Failed to extract latency stats"

    # Validate the latency against expected ranges
    assert expected_latency['min'][0] <= latency_stats['min'] <= expected_latency['min'][1], \
        f"{test_type.capitalize()} min latency is out of expected range"
    assert expected_latency['avg'][0] <= latency_stats['avg'] <= expected_latency['avg'][1], \
        f"{test_type.capitalize()} avg latency is out of expected range"
    assert expected_latency['max'][0] <= latency_stats['max'] <= expected_latency['max'][1], \
        f"{test_type.capitalize()} max latency is out of expected range"
