import subprocess
import pytest

def set_gpio_direction():
    command = f'echo out | sudo tee /sys/class/gpio/dummy0/direction'
    subprocess.run(command, shell=True, check=True)
    print("GPIO direction set to 'out'")

def write_gpio_value():
    command = f'echo 1 | sudo tee /sys/class/gpio/dummy0/value'
    subprocess.run(command, shell=True, check=True)
    print("GPIO pin set to 'high'")

def test_write_gpio_value():
    set_gpio_direction()

    write_gpio_value()

    command = f'cat /sys/class/gpio/dummy0/value'
    value = subprocess.check_output(command, shell=True).decode().strip()

    assert value == '1'

if __name__ == "__main__":
    pytest.main()

