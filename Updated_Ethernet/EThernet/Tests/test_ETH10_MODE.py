import subprocess 
from Inputs.common_inputs import Inputs

"THis test case is to verify whether the e1000 operates on promisc mode."

def test_promiscuous_mode():
    subprocess.run(["ip", "link", "set", Inputs.Interface, "promisc", "on"], check=True)
    result = subprocess.run(["ip", "link", "show", Inputs.Interface], capture_output=True, text=True)
    for line in result.stdout.splitlines():
       if "PROMISC" in line:
          print("\nPromisc mode on\n",line)
    assert "PROMISC" in result.stdout, f"Promiscuous mode not enabled on {Inputs.Interface}"
