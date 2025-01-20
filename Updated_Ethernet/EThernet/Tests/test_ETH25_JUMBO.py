import subprocess
import re
import pytest

"This test case is to verify whether the driver and NIC supports the jumbo frames"

def get_mtu(interface):
    """Returns the MTU of the network interface."""
    result = subprocess.run(['ip', 'addr', 'show', interface], capture_output=True, text=True)
    print(f"Output from ip addr show: {result.stdout}")  # Debugging output
    
    # Use regular expression to find the MTU value
    match = re.search(r'\s+mtu (\d+)', result.stdout)
    
    if match:
        mtu = int(match.group(1))
        return mtu
    else:
        raise ValueError(f"MTU not found for interface {interface}")

def get_ring_buffer(interface):
    """Returns the ring buffer settings (RX and TX jumbo) for the given interface."""
    result = subprocess.run(['ethtool', interface], capture_output=True, text=True)
    print(f"Output from ethtool {interface}: {result.stdout}")  # Debugging output

    rx_jumbo = None
    tx_jumbo = None

    # Check for RX and TX Jumbo settings in the ethtool output
    for line in result.stdout.splitlines():
        if "RX Jumbo" in line:
            rx_jumbo = line.split(":")[1].strip()
        if "TX Jumbo" in line:
            tx_jumbo = line.split(":")[1].strip()

    if rx_jumbo == "n/a" or tx_jumbo == "n/a":
        return None, None

    return rx_jumbo, tx_jumbo

def test_jumbo_frame_support():
    """Tests if the eth0 interface supports jumbo frames."""
    interface = 'eth0'
    
    # Check MTU
    try:
        mtu = get_mtu(interface)
        print(f"MTU for {interface}: {mtu}")
    except ValueError as e:
        print(e)
        mtu = None
    
    # Assert MTU >= 9000 to confirm jumbo frame support
    if mtu is None or mtu < 9000:
        pytest.fail(f"Jumbo frames not supported on {interface}. MTU is {mtu}")
    
    # Check jumbo frame settings
    try:
        rx_jumbo, tx_jumbo = get_ring_buffer(interface)
        if rx_jumbo is None or tx_jumbo is None:
            pytest.fail(f"Jumbo frames are not supported (RX Jumbo: {rx_jumbo}, TX Jumbo: {tx_jumbo})")
        else:
            print(f"RX Jumbo: {rx_jumbo}, TX Jumbo: {tx_jumbo}")
    except ValueError as e:
        print(f"Error while checking ring buffer settings: {e}")
        pytest.fail("Error while checking ring buffer settings.")
    
    # If jumbo frames are not supported, fail the test
    if rx_jumbo is None or tx_jumbo is None:
        pytest.fail("Jumbo frames are not supported.")

# Run the test
if __name__ == "__main__":
    pytest.main()
