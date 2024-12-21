import subprocess
import smbus2
import pytest
from Inputs.common_inputs import Inputs

"This test case is to verfy the functionality of reading from register by reading the low threshhold and high threshhold registers of lm75 "


# LM75 register addresses for low threshold, and high threshold
LOW_THRESHOLD_REG = 0x02
HIGH_THRESHOLD_REG = 0x03

def read_register(bus, address, reg):

    # Read a 16-bit word from the register (2 bytes)
    value = bus.read_word_data(address, reg)
    # Swap the bytes to get the correct order (little endian -> big endian)
    value = ((value & 0xFF) << 8) | ((value >> 8) & 0xFF)
    return value

# Convert the register value to a temperature (LM75 uses 0.0625°C per bit)
def register_to_temperature(value):
    return value / 256.0

def unload_lm75():

    print("\nunloading lm75 module for this test")
    result = subprocess.run(['sudo', 'modprobe', '-r', 'lm75'], capture_output=True, text=True)
    return result.returncode

def load_lm75():

    print("\nTest completed Again loading  lm75")
    subprocess.run(['sudo', 'modprobe', 'lm75'], check=True)


def test_temperature_thresholds():

    bus = smbus2.SMBus(Inputs.I2C_BUS)

    unload_lm75()

    # Read the low threshold register
    low_threshold = read_register(bus, Inputs.DEVICE_ADDR, LOW_THRESHOLD_REG)

    print(f"\nLow Threshold (Hex): {low_threshold:#04x}")  # Print in hex

    low_threshold_dec = low_threshold  # The value is already in decimal
    print(f"Low Threshold (Dec): {low_threshold_dec}")

    low_threshold_temp = register_to_temperature(low_threshold)
    print(f"Low Threshold (Celsius): {low_threshold_temp:.4f}°C")

    # Read the high threshold register
    high_threshold = read_register(bus, Inputs.DEVICE_ADDR, HIGH_THRESHOLD_REG)
    print(f"\nHigh Threshold (Hex): {high_threshold:#04x}")  # Print in hex

    high_threshold_dec = high_threshold  # The value is already in decimal
    print(f"High Threshold (Dec): {high_threshold_dec}")

    high_threshold_temp = register_to_temperature(high_threshold)
    print(f"High Threshold (Celsius): {high_threshold_temp:.4f}°C")

    assert low_threshold_temp > -55.0 and low_threshold_temp < 125.0, "Low threshold out of range"
    assert high_threshold_temp > -55.0 and high_threshold_temp < 125.0, "High threshold out of range"

    # Clean up
    bus.close()
    load_lm75()

if __name__ == "__main__":
    pytest.main()

