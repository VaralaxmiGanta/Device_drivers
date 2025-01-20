import subprocess
import sys

"This test case is to verify the device driver attachment to the device by checking systemctl status of lm75-bind.service"

def run_command(command):
    try:
        print(f"Running: {' '.join(command)}")
        result = subprocess.run(command, check=True, text=True, capture_output=True)
        print(result.stdout.strip())
    except subprocess.CalledProcessError as e:
        print(f"Error while executing: {' '.join(command)}", file=sys.stderr)
        print(e.stderr.strip(), file=sys.stderr)
        sys.exit(e.returncode)

def test_manage_lm75_service():

    print("Managing lm75-bind.service...")
    
    run_command(["sudo", "systemctl", "daemon-reload"])

    run_command(["sudo", "systemctl", "start", "lm75-bind.service"])

    # Enable the service to start on boot
    run_command(["sudo", "systemctl", "enable", "lm75-bind.service"])

    # Check the status of the service
    print("\nChecking service status...")
    run_command(["sudo", "systemctl", "status", "lm75-bind.service"])

if __name__ == "__main__":
    test_manage_lm75_service()

