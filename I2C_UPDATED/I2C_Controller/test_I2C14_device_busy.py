import subprocess
import smbus2
import pytest
from Inputs.common_inputs import Inputs

"This test case is to verify the Device or Resource busy condition when two process using the I2C device"

REGISTER_ADDR = 0X02

# Initialize the I2C bus
bus = smbus2.SMBus(Inputs.I2C_BUS)

def load_lm75():
    if 'lm75' not in subprocess.getoutput('lsmod'):
        subprocess.run(['sudo', 'modprobe', 'lm75'], check=True)

def unload_lm75():
    subprocess.run(['sudo', 'modprobe', '-r', 'lm75'], check=True)

def simulate_busy_condition():
    try:
        print("Performing first read to occupy the bus...")
        bus.read_byte_data(Inputs.DEVICE_ADDR, REGISTER_ADDR)
        print("Performing second read to detect busy bus condition...")
        bus.read_byte_data(Inputs.DEVICE_ADDR, REGISTER_ADDR)
        print("Second read succeeded.")
        return False
    except OSError as e:
        if e.errno == 16:  # Errno 16 corresponds to "Device or resource busy"
            print(f"Read failed: {e}")
            return True  # The device was busy
        raise

@pytest.mark.i2c
def test_device_busy():
    load_lm75()
    is_busy_detected = simulate_busy_condition()
    unload_lm75()

    # Fail the test if the busy condition is detected
    assert not is_busy_detected, "Test failed because the device is busy."

