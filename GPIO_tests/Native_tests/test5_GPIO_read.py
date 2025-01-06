import subprocess
import pytest

def read_gpio_value():
    command = f'cat /sys/class/gpio/dummy0/value'
    value = subprocess.check_output(command, shell=True).decode().strip()
    print(f"the value read from GPIO pin is {value}")
    return value

def test_read_gpio_value():
    value = read_gpio_value()
    assert value in ['0', '1'], f"Unexpected GPIO value: {value}"
