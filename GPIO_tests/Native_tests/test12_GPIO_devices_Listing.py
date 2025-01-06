import os
import pytest

def test_gpiochip_available():
    gpiochip_devices = [f for f in os.listdir("/dev/") if f.startswith("gpiochip")]

    print(f"Found gpiochip devices: {gpiochip_devices}")
    assert gpiochip_devices, "No gpiochip device found"

if __name__ == "__main__":
    pytest.main()

