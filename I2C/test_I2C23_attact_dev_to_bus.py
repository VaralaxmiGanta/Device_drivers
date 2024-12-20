import subprocess
import sys

def run_command(command):
    """
    Run a shell command and print its output. Exit if the command fails.
    """
    try:
        print(f"Running: {' '.join(command)}")
        result = subprocess.run(command, check=True, text=True, capture_output=True)
        print(result.stdout.strip())
    except subprocess.CalledProcessError as e:
        print(f"Error while executing: {' '.join(command)}", file=sys.stderr)
        print(e.stderr.strip(), file=sys.stderr)
        sys.exit(e.returncode)

def test_manage_lm75_service():
    """
    Reload, start, and enable the lm75-bind.service systemd service.
    """
    print("Managing lm75-bind.service...")
    
    # Reload systemd manager configuration
    run_command(["sudo", "systemctl", "daemon-reload"])

    # Start the service
    run_command(["sudo", "systemctl", "start", "lm75-bind.service"])

    # Enable the service to start on boot
    run_command(["sudo", "systemctl", "enable", "lm75-bind.service"])

    # Check the status of the service
    print("\nChecking service status...")
    run_command(["sudo", "systemctl", "status", "lm75-bind.service"])

if __name__ == "__main__":
    manage_lm75_service()

