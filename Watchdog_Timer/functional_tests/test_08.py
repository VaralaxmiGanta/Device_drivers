'''Check for a running process/daemon by its PID file,if it doesn't exists watchdog will trigger system reboot'''


from conftest import start_watchdog_service
import subprocess
import fileinput
import sys
import os

config_file_path="/etc/watchdog.conf"
pid_file="/var/run/sshd.pid"


def remove_pidfile():
    try:
        if os.path.exists(pid_file):
            subprocess.run(["sudo","rm",pid_file],check=True)
            print("sshd pid  file is removed")
    except Exception:
        print("file not exists to remove")

def modify_watchdog_config():
    try:
        with fileinput.FileInput(config_file_path, inplace=True, backup='.bak') as file:
            for line in file:
                if line.strip().startswith("#pidfile") or line.strip().startswith("# pidfile"):
                    print(f"pidfile = {pid_file}")
                else:
                    print(line, end='')

        print(f"sshd service pid {pid_file} is updated in {config_file_path}")
    
    except Exception as e:
        print(f"Failed to modify the configuration file: {e}")
        
def test_pidfile():
    remove_pidfile()    
    modify_watchdog_config()
    start_watchdog_service()
    print("Now watchdog will initiate reboot in 60sec")
    





