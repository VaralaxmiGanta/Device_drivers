import subprocess
import pytest
#from Inputs.common_inputs import Inputs

"""This test case is to change the speed and duplex of interface using ethtool"""

def get_speed_duplex(interface):
    result = subprocess.run(
        ['sudo','ethtool', interface],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True
    )
    output = result.stdout
    speed = duplex = None
    for line in output.splitlines():
        if 'Speed' in line:
            speed = line.split(":")[1].strip()
        if 'Duplex' in line:
            duplex = line.split(":")[1].strip()
    return speed, duplex

def test_ethtool_speed_duplex():

    interface =  "eth0"
    
    # Query current speed and duplex
    speed, duplex = get_speed_duplex(interface)
    print(f"Current Speed: {speed}, Current Duplex: {duplex}")

    # Set speed and duplex mode to 1000Mb/s and full duplex
    subprocess.run(['ethtool', '-s', interface, 'speed', '1000', 'duplex', 'full'])

    # Verify the changes
    new_speed, new_duplex = get_speed_duplex(interface)
    print(f"New Speed: {new_speed}, New Duplex: {new_duplex}")

    # Check if the settings were applied correctly
    assert new_speed == '1000Mb/s'
    assert new_duplex == 'Full'
