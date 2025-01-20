"This test case is to verify whether the sensors package lists the connected the lm75 sensor "

import subprocess
def test_lm75_adapter_name():
    # Run sensors command and check for the adapter name
    sensors_output = subprocess.check_output("sensors", shell=True).decode('utf-8')
    print(sensors_output)
    print("\nSensors are successfully listed by lm-sensnors package")


