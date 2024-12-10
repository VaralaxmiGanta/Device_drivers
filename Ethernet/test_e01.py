import subprocess
import pytest

"""This Test case is to check the dmesg output to validate initialization of Ethernet device during booting."""


def get_ethernet_initialization_messages():
    try:
        dmesg_output = subprocess.check_output(["sudo", "dmesg"], text=True)
        ethernet_init_msgs = [line for line in dmesg_output.splitlines() if 'eth' in line or 'e1000' in line]
        return ethernet_init_msgs

    except subprocess.CalledProcessError as e:
        print(f"Error executing command: {e}")
        return []


def test_ethernet_initialization():

    ethernet_init_msgs = get_ethernet_initialization_messages()
    ethernet_init_str = '\n'.join(ethernet_init_msgs)
    print("\nOUTPUT:\n", ethernet_init_str)

    assert ethernet_init_msgs, "No Ethernet initialization messages found in dmesg output."
    assert any("eth" in msg for msg in ethernet_init_msgs), \
        "Expected Ethernet interface message (eth) not found."
    assert any("Link is Up" in msg for msg in ethernet_init_msgs), \
        "Expected 'Link is Up' message not found in Ethernet initialization logs."

    print("Ethernet Initialization completed successfully with expected messages.")
