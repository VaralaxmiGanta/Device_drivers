import subprocess
from Inputs.common_inputs import Inputs

"THis test case is to check the ip address of eth0 interface"

def test_ip_assignment():
    result = subprocess.run(["ip", "addr", "show",Inputs.Interface], capture_output=True, text=True, check=True)
    for line in result.stdout.splitlines():
       if "inet" in line:
          print("IP Address :")
          print(line.strip().split()[1])
    assert "inet " in result.stdout, f"No IP address assigned to {Inputs.Interface}"
