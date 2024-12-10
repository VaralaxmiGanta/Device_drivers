import subprocess
import pytest


def check_ethtool(interface):
    """Check the current speed, duplex, and auto-negotiation settings using ethtool."""
    try:
        result = subprocess.run(['sudo', 'ethtool', interface], stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                                check=True)
        output = result.stdout.decode('utf-8')
        print(f"Current settings for {interface}:\n{output}")
        return output
    except subprocess.CalledProcessError as e:
        print(f"Error while running ethtool: {e.stderr.decode()}")
        return None


def set_ethtool(interface, speed, duplex, autoneg):
    """Set the speed, duplex, and autoneg using ethtool."""
    try:
        command = ['sudo', 'ethtool', '-s', interface, f'speed {speed}', f'duplex {duplex}', f'autoneg {autoneg}']
        subprocess.run(command, check=True)
        print(f"Successfully set {interface} to speed {speed}, duplex {duplex}, autoneg {autoneg}.")
    except subprocess.CalledProcessError as e:
        print(f"Error while setting ethtool parameters: {e.stderr.decode()}")
        raise


def verify_ethtool(interface, expected_speed, expected_duplex, expected_autoneg):
    """Verify the updated speed, duplex, and auto-negotiation settings using ethtool."""
    output = check_ethtool(interface)

    assert output is not None, "Failed to retrieve ethtool output"
    assert f"Speed: {expected_speed}Mb/s" in output, f"Expected speed {expected_speed}Mb/s not found in output"
    assert f"Duplex: {expected_duplex}" in output, f"Expected duplex {expected_duplex} not found in output"
    assert f"Auto-negotiation: {expected_autoneg}" in output, f"Expected auto-negotiation {expected_autoneg} not found in output"


@pytest.mark.parametrize(
    "interface, speed, duplex, autoneg",
    [
        ("eth0", "1000", "full", "on"),
        ("eth0", "1000", "full", "off"),
        ("eth0", "1000", "full", "off")
    ]
)
def test_ethtool(interface, speed, duplex, autoneg):
    """Test the ethtool settings by changing and verifying the configuration."""
    # Check initial settings
    print(f"Checking initial settings for {interface}...")
    check_ethtool(interface)

    # Set new settings
    print(f"Setting {interface} to speed {speed}, duplex {duplex}, autoneg {autoneg}...")
    set_ethtool(interface, speed, duplex, autoneg)

    # Verify the settings
    print(f"Verifying updated settings for {interface}...")
    verify_ethtool(interface, speed, duplex, autoneg)
