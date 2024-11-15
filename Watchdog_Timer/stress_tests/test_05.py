"""
Stress test for the watchdog under heavy system load. 
This test will simulate heavy CPU load while simultaneously interacting with the watchdog.

"""

import pytest
import os
import time
import multiprocessing
import threading

WATCHDOG_DEVICE_PATH = "/dev/watchdog"

@pytest.fixture
def setup_watchdog():
    if not os.path.exists(WATCHDOG_DEVICE_PATH):
        pytest.skip("Watchdog device not available")
    yield


def test_watchdog_integration_underheavy_system_load(setup_watchdog):
   def generate_cpu_load():
        """Generate CPU load by running computations in parallel."""
        while True:
            _ = [i * i for i in range(10000)] 

    def stress_watchdog():
        """Write heartbeats to the watchdog device continuously."""
        try:
            with open(WATCHDOG_DEVICE_PATH, 'w') as wd:
                while True:
                    wd.write("heartbeat")  
        except IOError as e:
            print(f"Error writing to the watchdog device: {e}")
            raise 

    processes = []
    stress_watchdog_thread = None

    try:
        for _ in range(4):  
            p = multiprocessing.Process(target=generate_cpu_load)
            p.start()
            processes.append(p)

        stress_watchdog_thread = threading.Thread(target=stress_watchdog)
        stress_watchdog_thread.start()

        time.sleep(60)  
    except Exception as e:
        pytest.fail(f"An error occurred during the stress test: {e}")
    finally:
        for p in processes:
            try:
                p.terminate() 
            except Exception as e:
                print(f"Error terminating process: {e}")
        
        if stress_watchdog_thread:
            try:
                stress_watchdog_thread.join()  
            except Exception as e:
                print(f"Error joining watchdog thread: {e}")

        print("Completed watchdog stress test under heavy load or with error handling.")

