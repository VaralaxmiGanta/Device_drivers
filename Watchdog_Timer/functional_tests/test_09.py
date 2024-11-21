"""
To monitors the temperature and triggers the watchdog timer if the temperature exceeds the defined threshold
"""

from conftest import start_watchdog_service
import time
import subprocess
import os
import fileinput

config_file_path = "/etc/watchdog.conf"
TEMP_SENSOR_PATH = "/sys/class/thermal/thermal_zone0/temp"
MAX_TEMP_THRESHOLD = 90  

def modify_watchdog_config():
    try:
        with fileinput.FileInput(config_file_path, inplace=True, backup='.bak') as file:
            for line in file:
                if line.strip().startswith("temperature") or :
                    print(f"temperature_sensor = {TEMP_SENSOR_PATH}")
                else:
                    print(line, end='')
                if line.strip().startswith('max-temperature'):
                    print(f"max-temperature = {MAX_TEMP_THRESHOLD}")
                else:
                    print(line,end='')
        print(f"maximum temperature of {MAX_TEMP_THRESHOLD } and temperature_sensor path {TEMP_SENSOR_PATH} are updated in {config_file_path}")
    
    except Exception as e:
        print(f"Failed to modify the configuration file: {e}")



def test_temperature_sensor():
    modify_watchdog_config()
    start_watchdog_service()
    print("Watchdog will initiate reboot when the temperature exceeds the threshold temperature")

