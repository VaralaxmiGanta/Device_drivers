
'''Check for the reboot triggering when test-binary returns exit code other than 0. This test-binary will execute automatically when watchdog service starts. In this test the test-binary returns exit code 1,so watchdog will trigger reboot'''


import subprocess
import fileinput
import sys

config_file_path="/etc/watchdog.conf"
file1="etc/watchdog.d/file1.py"




def modify_watchdog_config():
    try:
        with fileinput.FileInput(config_file_path, inplace=True, backup='.bak') as file:
            for line in file:
                if line.strip().startswith("#test-binary") or line.strip().startswith("# test-binary"):
                    print(f"test-binary = {file1}")
                elif line.strip().startswith("#test-directory") or line.strip().startswith("# test-directory"):
                    print("test-directory = /etc/watchdog.d")
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


def test_testbinary():
    modify_watchdog_config()
    restart_watchdog_service()
    print("Now watchdog will initiate reboot in 60sec")    

