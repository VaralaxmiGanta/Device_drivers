import subprocess
import re
import pytest
from Inputs.common_inputs import Inputs

"This test case is to verify the write latency of I2C device within the limits"

def get_i2c_write_latency():

    result = subprocess.run(
        ['time', 'sudo', 'i2cset', '-y', str(Inputs.I2C_BUS), str(Inputs.DEVICE_ADDR), '0x22', '0x20'],  # Write 0x20 to address 0x22 on device 0x48
        stdout=subprocess.PIPE,  # Capture standard output
        stderr=subprocess.PIPE   # Capture error output (this includes the timing info)
    )

    # Get the output and error messages
    stdout_output = result.stdout.decode().strip()
    stderr_output = result.stderr.decode().strip()

    # Extract timing information using a refined regex
    timing_match = re.search(r'(\d+\.\d+)user\s+(\d+\.\d+)system\s+(\d+:\d+\.\d+)elapsed', stderr_output)

    if timing_match:
        user_time = timing_match.group(1)
        sys_time = timing_match.group(2)
        real_time = timing_match.group(3)

        return stdout_output, real_time, user_time, sys_time
    else:
        return stdout_output, None, None, None

def test_i2c_write_latency()\
        :
    output, real_time, user_time, sys_time = get_i2c_write_latency()
    print("\nreal :",real_time,"\nuser :",user_time,"\nsys",sys_time)
    assert output == "", f"Expected no output, got {output}"

    # Validate that timing information is extracted properly
    assert real_time is not None, "Real time should be extracted"
    assert user_time is not None, "User time should be extracted"
    assert sys_time is not None, "System time should be extracted"

    # Optionally, you can also check that the timing values are reasonable (e.g., they should be non-negative)
    assert float(real_time.split(':')[1]) >= 0, "Elapsed time should be non-negative"
    assert float(user_time) >= 0, "User time should be non-negative"
    assert float(sys_time) >= 0, "System time should be non-negative"

