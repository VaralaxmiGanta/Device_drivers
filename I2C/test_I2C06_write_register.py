import smbus2
import pytest
import time

# Define the I2C bus and the device address
I2C_BUS = 0  # This is usually 0 or 1, depending on your system
DEVICE_ADDR = 0x48  # LM75 device address

# LM75 register addresses for temperature, low threshold, and high threshold
LOW_THRESHOLD_REG = 0x02
HIGH_THRESHOLD_REG = 0x03

# Function to read a 16-bit register value
def read_register(bus, address, reg):
    # Read a 16-bit word from the register (2 bytes)
    value = bus.read_word_data(address, reg)
    # Swap the bytes to get the correct order (little endian -> big endian)
    value = ((value & 0xFF) << 8) | ((value >> 8) & 0xFF)
    return value

# Function to write a 16-bit value to a register
def write_register(bus, address, reg, value):
    # Write a 16-bit word to the register (2 bytes)
    # Swap the bytes to send the value in big endian
    value = ((value & 0xFF) << 8) | ((value >> 8) & 0xFF)
    bus.write_word_data(address, reg, value)

# Convert the register value to a temperature (LM75 uses 0.0625°C per bit)
def register_to_temperature(value):
    return value / 256.0

# Test writing and reading the low and high thresholds
def test_temperature_thresholds():
    bus = smbus2.SMBus(I2C_BUS)

    # Read current low threshold before writing new value
    current_low_threshold = read_register(bus, DEVICE_ADDR, LOW_THRESHOLD_REG)
    print(f"\nCurrent Low Threshold (Hex): {current_low_threshold:#04x}")
    #print(f"Current Low Threshold (Dec): {current_low_threshold}")
    print(f"Current Low Threshold (Celsius): {register_to_temperature(current_low_threshold):.4f}°C")

    # Read current high threshold before writing new value
    current_high_threshold = read_register(bus, DEVICE_ADDR, HIGH_THRESHOLD_REG)
    print(f"\nCurrent High Threshold (Hex): {current_high_threshold:#04x}")
    #print(f"Current High Threshold (Dec): {current_high_threshold}")
    print(f"Current High Threshold (Celsius): {register_to_temperature(current_high_threshold):.4f}°C")

    # Write new low threshold (e.g., 25.0°C -> 25 * 256 = 6400)
    new_low_threshold = 8400  # 25°C
    write_register(bus, DEVICE_ADDR, LOW_THRESHOLD_REG, new_low_threshold)
    #print(f"\nNew Low Threshold (Hex): {new_low_threshold:#04x}")
    #print(f"New Low Threshold (Dec): {new_low_threshold}")
    #print(f"New Low Threshold (Celsius): {register_to_temperature(new_low_threshold):.4f}°C")

    # Write new high threshold (e.g., 80.0°C -> 80 * 256 = 20480)
    new_high_threshold = 10580  # 80°C
    write_register(bus, DEVICE_ADDR, HIGH_THRESHOLD_REG, new_high_threshold)
    #print(f"\nNew High Threshold (Hex): {new_high_threshold:#04x}")
    #print(f"New High Threshold (Dec): {new_high_threshold}")
    #print(f"New High Threshold (Celsius): {register_to_temperature(new_high_threshold):.4f}°C")

    # Read back the low threshold register after writing
    low_threshold = read_register(bus, DEVICE_ADDR, LOW_THRESHOLD_REG)
    print(f"\nLow Threshold after write (Hex): {low_threshold:#04x}")
    #print(f"Low Threshold after write (Dec): {low_threshold}")
    print(f"Low Threshold after write (Celsius): {register_to_temperature(low_threshold):.4f}°C")

    # Read back the high threshold register after writing
    high_threshold = read_register(bus, DEVICE_ADDR, HIGH_THRESHOLD_REG)
    print(f"\nHigh Threshold after write (Hex): {high_threshold:#04x}")
    #print(f"High Threshold after write (Dec): {high_threshold}")
    print(f"High Threshold after write (Celsius): {register_to_temperature(high_threshold):.4f}°C")


    # Clean up
    bus.close()

# Run the test
if __name__ == "__main__":
    pytest.main()

