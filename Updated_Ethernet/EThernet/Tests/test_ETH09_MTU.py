import subprocess
from Inputs.common_inputs import Inputs

"THis test case is to verify the changing of MTU size"

def test_mtu_configuration():
    mtu_size = "2500"
    subprocess.run(["ip", "link", "set",Inputs.Interface, "mtu", mtu_size], check=True)
    result = subprocess.run(["ip", "link", "show", Inputs.Interface], capture_output=True, text=True)
    for line in result.stdout.splitlines():
       if "mtu" in line:
          print(f"\n MTU size changed to {mtu_size} : \n",line)
    assert f"mtu {mtu_size}" in result.stdout, f"Failed to set MTU {mtu_size} on {Inputs.Interface}"
