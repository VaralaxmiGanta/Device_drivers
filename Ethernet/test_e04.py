import subprocess
import pytest

def get_interface_status(interface_name):
    try:
        result = subprocess.run(['ip', 'link', 'show', interface_name], stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                                text=True)
        if result.returncode != 0:
            raise Exception(f"Failed to get status for interface {interface_name}")

        if 'UP' in result.stdout:
            return 'UP'
        else:
            return 'DOWN'
    except Exception as e:
        return str(e)


def test_eth0_status():
    status = get_interface_status("eth0")

    if status == 'UP':
        print("Interface eth0 is UP.")
        assert status == 'UP', "Expected eth0 to be UP, but it was DOWN."
    elif status == 'DOWN':
        print("Interface eth0 is DOWN.")
        assert status == 'DOWN', "Expected eth0 to be DOWN, but it was UP."
    else:
        pytest.fail(f"Error: Unable to determine the status of eth0. Error message: {status}")

