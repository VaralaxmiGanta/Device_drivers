import subprocess
import pytest
from Inputs.common_inputs import Inputs


"""This test case is to verify whether the network statistics can be fetched using ethtool."""

def get_ethtool_stats(interface):
    result = subprocess.run(
        ['ethtool', '-S', interface],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True
    )
    return result.stdout

def test_ethtool_stats():
    interface = Inputs.Interface
    stats = get_ethtool_stats(interface)
    print("\n Statistics fetched using ethtool\n",stats)    
    assert "rx_packets" in stats
    assert "tx_packets" in stats
    assert "rx_bytes" in stats
    assert "tx_bytes" in stats
