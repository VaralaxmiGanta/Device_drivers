import subprocess
#from Inputs.common_inputs import Inputs

"""THis test case is to verify whether the auto negotiation is on for best connectivity if it is off then turn to on."""

def check_auto_negotiation_status(interface):
    """Helper function to check the current auto-negotiation status."""
    command = f"ethtool {interface}"
    result = subprocess.run(command, shell=True, capture_output=True, text=True)
    
    if result.returncode != 0:
        raise Exception(f"Failed to get ethtool status for {interface}: {result.stderr}")
    
    for line in result.stdout.splitlines():
        if "Auto-negotiation" in line:
            return "on" if "on" in line else "off"
    raise ValueError("Auto-negotiation status not found.")

def enable_auto_negotiation(interface):
    """Helper function to turn on auto-negotiation if it's off."""
    print(f"Checking auto-negotiation status for {interface}...")
    current_status = check_auto_negotiation_status(interface)
    print(f"Initial Auto-negotiation status for {interface}: {current_status}")

    if current_status == "off":
        print(f"Auto-negotiation is currently OFF. Turning it ON...")
        command = f"sudo ethtool -s {interface} autoneg on"
        result = subprocess.run(command, shell=True, capture_output=True, text=True)
        
        if result.returncode != 0:
            raise Exception(f"Failed to enable auto-negotiation for {interface}: {result.stderr}")
        
        print(f"Auto-negotiation for {interface} is now set to ON.")
    else:
        print(f"Auto-negotiation is already ON for {interface}.")

def test_auto_negotiation():
    """Test case to check if auto-negotiation is on, if not, turn it on."""
    interface = "eth0"

    enable_auto_negotiation(interface)

    final_status = check_auto_negotiation_status(interface)
    print(f"Final Auto-negotiation status for {interface}: {final_status}")
    
    assert final_status == "on", f"Auto-negotiation should be ON, but it is {final_status}."
