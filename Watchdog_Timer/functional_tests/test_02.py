'''Edit the config file(/etc/watchdog.conf).
watchdog-device		= /dev/watchdog
watchdog-timeout	= 60
realtime		= yes
priority		= 1
ping			= 8.8.8.8
ping-count		= 3
interface		= eth0'''


  
import subprocess

def test_simulate_network_failure_in_host():
    try:
        interface = 'eth0'
        command = f"sudo ip link set {interface} down"
        result = subprocess.run(command, shell=True, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        
        if result.returncode == 0:
            print(f"Network interface {interface} is down.")
        else:
            print(f"Failed to bring {interface} down. Exit code: {result.returncode}")
    
    except subprocess.CalledProcessError as e:
        print(f"Command failed with error: {e}")
    except Exception as ex:
        print(f"An unexpected error occurred: {ex}")

