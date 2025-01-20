import subprocess
import smbus2
import pytest
import time
from Inputs.common_inputs import Inputs


"This test case is to verfy the functionality of writing to  register by writing to the low threshhold and high threshhold registers of lm75 "


# LM75 register addresses for temperature, low threshold, and high threshold
LOW_THRESHOLD_REG = 0x02
HIGH_THRESHOLD_REG = 0x03

# Function to read a 16-bit register value
def read_register(bus, address, reg):
    value = bus.read_word_data(address, reg)
    # Swap the bytes to get the correct order (little endian -> big endian)
    value = ((value & 0xFF) << 8) | ((value >> 8) & 0xFF)
    return value

# Function to write a 16-bit value to a register
def write_register(bus, address, reg, value):
    # Swap the bytes to send the value in big endian
    value = ((value & 0xFF) << 8) | ((value >> 8) & 0xFF)
    bus.write_word_data(address, reg, value)

# Convert the register value to a temperature (LM75 uses 0.0625°C per bit)
def register_to_temperature(value):
    return value / 256.0

def unload_lm75():
    print("\nunloading lm75 module for this test")
    result = subprocess.run(['sudo', 'modprobe', '-r', 'lm75'], capture_output=True,text=True)
    return result.returncode

def load_lm75():
    print("\nTest completed Again loading  lm75")
    subprocess.run(['sudo', 'modprobe', 'lm75'], check=True)

def test_temperature_thresholds():
    bus = smbus2.SMBus(Inputs.I2C_BUS)
    unload_lm75()

    # Read current low threshold before writing new value
    current_low_threshold = read_register(bus, Inputs.DEVICE_ADDR, LOW_THRESHOLD_REG)
    print(f"\nCurrent Low Threshold (Hex): {current_low_threshold:#04x}")
    print(f"Current Low Threshold (Celsius): {register_to_temperature(current_low_threshold):.4f}°C")

    # Read current high threshold before writing new value
    current_high_threshold = read_register(bus, Inputs.DEVICE_ADDR, HIGH_THRESHOLD_REG)
    print(f"\nCurrent High Threshold (Hex): {current_high_threshold:#04x}")
    print(f"Current High Threshold (Celsius): {register_to_temperature(current_high_threshold):.4f}°C")

    # Write new low threshold (e.g., 25.0°C -> 25 * 256 = 6400)
    new_low_threshold = 8400  # 25°C
    write_register(bus, Inputs.DEVICE_ADDR, LOW_THRESHOLD_REG, new_low_threshold)

    # Write new high threshold (e.g., 80.0°C -> 80 * 256 = 20480)
    new_high_threshold = 10580  # 80°C
    write_register(bus, Inputs.DEVICE_ADDR, HIGH_THRESHOLD_REG, new_high_threshold)

    # Read back the low threshold register after writing
    low_threshold = read_register(bus, Inputs.DEVICE_ADDR, LOW_THRESHOLD_REG)
    print(f"\nLow Threshold after write (Hex): {low_threshold:#04x}")
    print(f"Low Threshold after write (Celsius): {register_to_temperature(low_threshold):.4f}°C")

    # Read back the high threshold register after writing
    high_threshold = read_register(bus, Inputs.DEVICE_ADDR, HIGH_THRESHOLD_REG)
    print(f"\nHigh Threshold after write (Hex): {high_threshold:#04x}")
    print(f"High Threshold after write (Celsius): {register_to_temperature(high_threshold):.4f}°C")


    # Clean up
    bus.close()
    load_lm75()

if __name__ == "__main__":
    pytest.main()

