import subprocess

def check_link_status(interface):
    try:
        result = subprocess.run(["ethtool", interface], capture_output=True, text=True, check=True)
        for line in result.stdout.splitlines():
            if "Link detected:" in line:
                status = line.split(":")[1].strip()
                return "up" if status == "yes" else "down"
    except FileNotFoundError:
        return "ethtool not found. Please install it using 'sudo apt install ethtool'."
    except subprocess.CalledProcessError:
        return f"Failed to get link status for interface {interface}. Ensure it exists and is configured."
    except Exception as e:
        return f"An error occurred: {e}"

# Specify the interface
interface = "eth0"
status = check_link_status(interface)
print(f"Link status of {interface}: {status}")
