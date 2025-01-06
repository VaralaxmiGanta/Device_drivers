import subprocess
import pytest

def set_gpio_output():
    # Set the GPIO direction to 'in'
    command = 'echo in | sudo tee /sys/class/gpio/dummy0/direction'
    subprocess.run(command, shell=True, check=True)
    print("GPIO pin direction set to 'in'")

def test_set_gpio_output():
    set_gpio_output()
   
    direction = subprocess.check_output(
        'cat /sys/class/gpio/dummy0/direction', shell=True
    ).decode().strip()
   
    assert direction == 'in'

if __name__ == "__main__":
    pytest.main()

