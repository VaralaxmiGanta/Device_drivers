import time
import subprocess

def set_gpio_direction():
    command = f'echo out | sudo tee /sys/class/gpio/dummy0/direction'
    subprocess.run(command, shell=True, check=True)
    print("GPIO direction set to 'out'")

def write_gpio_value(value):
    set_gpio_direction()
    subprocess.run(f'echo {value} | sudo tee /sys/class/gpio/dummy0/value', shell=True)

def read_gpio_value():
    value = subprocess.check_output(f'cat /sys/class/gpio/dummy0/value', shell=True).decode().strip()
    return value

def test_detect_gpio_edge():
    last_value = read_gpio_value()
    print(f"Initial GPIO value: {last_value}")
    

    for i in range(6):
        # Toggle GPIO value
        current_value = '1' if i % 2 == 0 else '0'
        write_gpio_value(current_value)

        new_value = read_gpio_value()
        print(f"GPIO value after toggle: {new_value}")

        if new_value != last_value:
            if new_value == '1':
                assert new_value == '1' and last_value == '0', "Rising edge not detected correctly"
                print("Rising edge detected.")
            elif new_value == '0':
                assert new_value == '0' and last_value == '1', "Falling edge not detected correctly"
                print("Falling edge detected.")
        

        last_value = new_value

        time.sleep(0.1)

if __name__ == "__main__":
    pytest.main()
