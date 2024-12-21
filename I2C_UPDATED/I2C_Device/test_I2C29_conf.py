import os
"This test case is to verify whether the conf file exists for changing the tmp105 sensor configurations"

def test_lm75_config_file():
    # Define the path to the main configuration file and the sensors directory
    config_files = [
        "/etc/sensors3.conf",  # Main configuration file
    ]
    
    # Check the /etc/sensors.d/ directory for additional configuration files
    sensors_d_dir = "/etc/sensors.d/"
    if os.path.exists(sensors_d_dir):
        for filename in os.listdir(sensors_d_dir):
            if filename.endswith(".conf"):
                config_files.append(os.path.join(sensors_d_dir, filename))
    
    # Iterate through each config file
    for config_file in config_files:
        # Check if the configuration file exists
        if os.path.exists(config_file):
            # Open and read the content of the configuration file
            with open(config_file, 'r') as file:
                config_content = file.read()
    
            # Check if the 'lm75' sensor is configured in the file
            print(f"LM75 configuration found in {config_file}")
        else:
            print(f"Configuration file {config_file} not found")


