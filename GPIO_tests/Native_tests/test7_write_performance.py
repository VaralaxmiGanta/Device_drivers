import subprocess
import time
import pytest

def set_gpio_direction():
    command = f'echo out | sudo tee /sys/class/gpio/dummy0/direction'
    subprocess.run(command, shell=True, check=True)
    print("GPIO direction set to 'out'")

def measure_gpio_write_performance (count=10):
    start_time = time.time()
    for _ in range(count):
        # Writing high value (1) to GPIO pin
        cmd = 'echo 1 | sudo tee /sys/class/gpio/dummy0/value'
        subprocess.run(cmd, shell=True, check=True)
    end_time = time.time()
    
    elapsed_time = end_time - start_time
    print(f"GPIO Write Performance: {elapsed_time:.4f} seconds for {count} writes")
    return elapsed_time

def test_measure_gpio_write_performance():
    set_gpio_direction()
    elapsed_time = measure_gpio_write_performance()

    assert elapsed_time < 5.0, f"GPIO write performance is too slow: {elapsed_time} seconds"

if __name__ == "__main__":
    pytest.main()

