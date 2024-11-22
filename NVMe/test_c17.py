import subprocess
import time
import pytest

"""This Test case is to verify that whether the driver reinitializes the nvme device after performing controller reset"""

def perform_controller_reset():
    print("\nSimulating NVMe controller reset...")
    subprocess.run(['sudo', 'nvme', 'reset', '/dev/nvme0'], check=True)

def check_dmesg_for_reset():
    print("\nChecking dmesg logs for controller reset...")
    result = subprocess.run("sudo dmesg | grep nvme", capture_output=True, text=True,shell=True)
    reset_logs = [line for line in result.stdout.splitlines() if "resetting controller" in line.lower()]
    
    if reset_logs:
        print("\nController reset detected in dmesg:")
        for log in reset_logs:
            print(log)
        return True
    else:
        print("\nController reset not found in dmesg.")
        return False

def check_queue_reinitialization():
    print("\nChecking if NVMe queues are reinitialized...")
    result = subprocess.run("sudo dmesg | grep nvme", capture_output=True, text=True,shell=True)
    queue_logs = [line for line in result.stdout.splitlines() if "read/poll queues" in line.lower()]
    
    if queue_logs:
        print("\nQueue reinitialization detected in dmesg:")
        for log in queue_logs:
            print(log)
        return True
    else:
        print("Queue reinitialization not detected.")
        return False

def test_controller_reset_recovery():
    fio_process = subprocess.Popen(['fio', '--name=test', '--rw=randwrite', '--ioengine=libaio', '--bs=4k', '--numjobs=4', '--iodepth=32', '--runtime=60', '--direct=1', '--filename=/dev/nvme0n1'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    perform_controller_reset()
    time.sleep(5)

    assert check_dmesg_for_reset(), "Controller reset not found in dmesg"
    assert check_queue_reinitialization(), "Queue reinitialization not detected in dmesg"

    stdout, stderr = fio_process.communicate()
    if "I/O error" in stderr.decode():
        print("I/O error detected after reset. Testing recovery.")
        recovery_test = subprocess.run(['lsblk', '/dev/nvme0n1'], capture_output=True, text=True)
        assert recovery_test.returncode == 0, "Device not accessible after reset"
        print("Device successfully reinitialized.")
    else:
        print("\nI/O operations were successful after controller reset.")

if __name__ == "__main__":
    pytest.main()
