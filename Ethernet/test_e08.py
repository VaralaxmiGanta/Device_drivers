import subprocess


def run_ethtool(interface):
    try:
        command = f"ethtool -S {interface}"
        result = subprocess.run(
            command, shell=True, text=True, capture_output=True, check=True
        )
        return result.stdout.strip()
    except subprocess.CalledProcessError as e:
        return f"Failed to fetch statistics for {interface}. Error: {e.stderr.strip()}"


def test_run_ethtool():
    interface = "eth0"  # Replace with a valid interface for your system

    # Run the function to get statistics
    result = run_ethtool(interface)

    # Example assertions
    assert "rx_packets" in result, "Failed to find rx_packets in statistics"
    assert "tx_packets" in result, "Failed to find tx_packets in statistics"
    assert "rx_bytes" in result, "Failed to find rx_bytes in statistics"
    assert "tx_bytes" in result, "Failed to find tx_bytes in statistics"

    # Example assertion to check non-zero values (optional)
    assert "rx_errors" in result and "0" in result, "Expected rx_errors to be 0"
    assert "tx_errors" in result and "0" in result, "Expected tx_errors to be 0"

    # Optionally print the result (for debugging purposes)
    print(f"Statistics for {interface}:\n{result}")

