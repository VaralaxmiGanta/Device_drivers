'''Check for a file existence in specified path,if it doesn't exists watchdog will trigger system reboot'''



import subprocess
import fileinput
import sys

config_file_path="/etc/watchdog.conf"
file1="/home/debian/file1"


def remove_pidfile():
    try:
        if not (subprocess.run(["file",file1],check=True)):
            subprocess.run(["rm",file1],check=True)
            print("file is removed")
    except Exception:
        print("file not exists to remove")



def modify_watchdog_config():
    try:
        with fileinput.FileInput(config_file_path, inplace=True, backup='.bak') as file:
            for line in file:
                if line.strip().startswith("#file") or line.strip().startswith("# file"):
                    print(f"file = {file1}")
                else:
                    print(line, end='')

        print(f"file {file1} is updated in {config_file_path}")
    
    except Exception as e:
        print(f"Failed to modify the configuration file: {e}")

def restart_watchdog_service():
    try:
        subprocess.run(["sudo", "systemctl", "stop", "watchdog"], check=True)        
        subprocess.run(["sudo", "systemctl", "start", "watchdog"], check=True)
        print("Watchdog service restarted successfully.")
    
    except subprocess.CalledProcessError as e:
        print(f"Failed to restart the watchdog service: {e}")

        
def test_pidfile():
    modify_watchdog_config()
    restart_watchdog_service()
    remove_pidfile()
    print("Now watchdog will initiate reboot in 60sec")
    





