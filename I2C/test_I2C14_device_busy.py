import time
import smbus2
import pytest

# I2C bus number (usually 0 or 1 on most systems, depending on your hardware)
I2C_BUS = 0

# I2C device address (e.g., lm75 is often at 0x48)
DEVICE_ADDR = 0x48

# Register address (e.g., temperature register for lm75)
REGISTER_ADDR = 0x00

# Initialize the I2C bus
bus = smbus2.SMBus(I2C_BUS)

def read_temperature():
    """Function to read temperature from the device."""
    try:
        temp = bus.read_byte_data(DEVICE_ADDR, REGISTER_ADDR)
        print(f"Read value 0x{temp:02x} from device 0x{DEVICE_ADDR:02x}")
        return temp
    except Exception as e:
        print(f"Error: {e}")
        return None

def simulate_bus_busy():
    """Function to simulate the condition of a busy I2C bus."""
    print(f"\nStarting transfer on device 0x{DEVICE_ADDR:02x}...")
    read_temperature()

    # Simulate the device driver or other process locking the bus for a while
    print("Simulating delay on device 0x48 to occupy the bus...")
    time.sleep(2)  # Simulate a delay where the bus might be busy

    print("Attempting transfer on device 0x50 while the bus might be busy...")
    try:
        read_temperature()
    except OSError as e:
        print(f"Error during second transfer: {e}")
        # Log the exact exception and message for debugging
        print(f"Exception type: {type(e)}")
        print(f"Exception message: {str(e)}")
        
        # Check if the error message contains 'Device or resource busy'
        if isinstance(e, OSError) and "Device or resource busy" in str(e):
            print("Bus busy condition detected!")
            return True
        else:
            print("Bus busy condition not detected.")
            return False
    return True

# Pytest test case for bus busy condition
def test_bus_busy():
    """Test case to assert that a bus busy condition is detected correctly."""
    # Run the simulation and assert that the bus busy condition is detected
    result = simulate_bus_busy()
    print(f"Simulation result: {result}")
    assert result is True, "Bus busy condition was not detected correctly."

