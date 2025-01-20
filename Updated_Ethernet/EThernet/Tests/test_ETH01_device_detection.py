import subprocess
import pytest

"""This Test case checks dmesg output for Ethernet device initialization during boot."""


def get_ethernet_initialization_messages():
    try:
        dmesg_output = subprocess.check_output(["sudo", "dmesg"], text=True)
        return [line for line in dmesg_output.splitlines() if 'eth' in line or 'e1000' in line]
    except subprocess.CalledProcessError:
        return []


def test_ethernet_initialization():
    ethernet_init_msgs = get_ethernet_initialization_messages()
    assert ethernet_init_msgs, "No Ethernet initialization messages found in dmesg output."

    print("\nEthernet Initialization Messages:\n" + '\n'.join(ethernet_init_msgs))
    print("Ethernet Initialization validation passed.")
