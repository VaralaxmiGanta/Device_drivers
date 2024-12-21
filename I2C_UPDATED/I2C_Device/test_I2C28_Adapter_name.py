"This test case is to check the adapter name of I2C controller"

import subprocess
def test_lm75_adapter_name():
    # Run sensors command and check for the adapter name
    sensors_output = subprocess.check_output("sensors", shell=True).decode('utf-8')
    print(sensors_output)
    assert "SMBus PIIX4 adapter" in sensors_output, "LM75 adapter not found in sensors output"

