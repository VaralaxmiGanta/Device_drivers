import subprocess
import pytest

"This test case is to check the dmeg logs for lm75 sensor detection"

def get_dmesg_logs():
    try:
        dmesg_output = subprocess.check_output(["dmesg"], universal_newlines=True)
        return dmesg_output
    except subprocess.CalledProcessError as e:
        pytest.fail(f"Error running dmesg: {e}")
    except Exception as e:
        pytest.fail(f"Unexpected error: {e}")

def test_lm75_detection_in_dmesg():
    dmesg_logs = get_dmesg_logs()

    # Print the dmesg logs containing 'lm75'
    lm75_logs = [line for line in dmesg_logs.splitlines() if 'lm75' in line]
    print("\n".join(lm75_logs))  # Print out the logs related to lm75 sensor

    # Assert the lm75 sensor is detected in the logs
    assert 'lm75' in dmesg_logs, "LM75 sensor not detected in dmesg logs"

    # Optionally check for specific sensor instantiations and assert
    assert 'i2c-0: new_device: Instantiated device lm75 at 0x48' in dmesg_logs, "LM75 sensor not instantiated at address 0x48"
    assert 'hwmon0: sensor \'lm75\'' in dmesg_logs, "LM75 sensor not detected as hwmon0"


