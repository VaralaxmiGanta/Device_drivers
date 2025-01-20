import subprocess
import time
import pytest

def measure_gpio_read_performance (count=10):
    start_time = time.time()
    for _ in range(count):
        # Writing high value (1) to GPIO pin
        cmd = 'cat /sys/class/gpio/dummy0/value'
        subprocess.run(cmd, shell=True, check=True)
    end_time = time.time()

    elapsed_time = end_time - start_time
    print(f"GPIO Read Performance: {elapsed_time:.4f} seconds for {count} writes")
    return elapsed_time

def test_measure_gpio_read_performance():
    elapsed_time = measure_gpio_read_performance()

    assert elapsed_time < 2.0, f"GPIO read performance is too slow: {elapsed_time} seconds"

if __name__ == "__main__":
    pytest.main()

