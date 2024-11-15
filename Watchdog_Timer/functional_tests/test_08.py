'''Check for a running process/daemon by its PID file,if it doesn't exists watchdog will trigger system reboot'''



import subprocess
import fileinput
import sys

config_file_path="/etc/watchdog.conf"
pid_file="/var/run/sshd.pid"


def remove_pidfile():
    try:
        if not (subprocess.run(["file",pid_file],check=True)):
            subprocess.run(["rm",pid_file],check=True)
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

def restart_watchdog_service():
    try:
        subprocess.run(["sudo", "systemctl", "stop", "watchdog"], check=True)        
        subprocess.run(["sudo", "systemctl", "start", "watchdog"], check=True)
        print("Watchdog service restarted successfully.")
    
    except subprocess.CalledProcessError as e:
        print(f"Failed to restart the watchdog service: {e}")

        
def test_pidfile():
    config_file_path = "/etc/watchdog.conf"
    modify_watchdog_config()
    restart_watchdog_service()
    remove_pidfile()
    print("Now watchdog will initiate reboot in 60sec")
    





