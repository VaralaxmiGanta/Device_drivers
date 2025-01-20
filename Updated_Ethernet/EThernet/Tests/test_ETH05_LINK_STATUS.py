import pytest
import subprocess
from Inputs.common_inputs import Inputs

"""This test case is to verify whether the link is detected for connectivity"""

def test_link_status():

    result = subprocess.run(["sudo","ethtool", Inputs.Interface], capture_output=True, text=True, check=True)
    for line in result.stdout.splitlines():
        if "Link detected:" in line:
            status = line.split(":")[1].strip()
            assert status == "yes", f"Link is not detected on {Inputs.Interface}"
            print(f"Link is detected on {Inputs.Interface}, status is 'up'.")
