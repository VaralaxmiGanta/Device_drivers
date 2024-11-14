'''This test will repeatedly start and stop the watchdog service to ensure that the driver can handle multiple restarts without failures.'''


import subprocess
import time
import pytest

def test_watchdog_service_restart():
    """Stress test to start and stop the watchdog service repeatedly."""
    
    try:
        for i in range(100):  # Restart the service 100 times
            print(f"Restarting watchdog service, iteration {i + 1}")
            subprocess.run(['sudo', 'systemctl', 'stop', 'watchdog'], check=True)
            time.sleep(1)
            subprocess.run(['sudo', 'systemctl', 'start', 'watchdog'], check=True)
            time.sleep(1)
        print("Watchdog service restarted 100 times successfully.")
    except subprocess.CalledProcessError as e:
        pytest.fail(f"Error during restarting watchdog service: {e}")
