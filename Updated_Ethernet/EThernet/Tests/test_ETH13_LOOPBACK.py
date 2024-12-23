import subprocess
import pytest

"""This test case is to verify whether pinging to loopback ip is successfull."""

@pytest.fixture
def ping_localhost():
    target_ip = "127.0.0.1"
    print(f"Pinging {target_ip} to verify network connectivity...")
    result = subprocess.run(
        ["ping", "-c", "4", target_ip], capture_output=True, text=True
    )
    yield result

def test_ping_localhost(ping_localhost):
    result = ping_localhost
    print(result.stdout)

    # Assert that the ping was successful
    assert result.returncode == 0, "Ping to localhost failed."

    # Check if the output contains a successful ping message
    assert "4 packets transmitted, 4 received" in result.stdout, "Packet loss detected during ping to localhost."
    print("Test Passed: Localhost ping successful.")
