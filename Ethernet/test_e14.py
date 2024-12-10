import subprocess


def run_command(command):
    try:
        result = subprocess.run(
            command, shell=True, text=True, capture_output=True, check=True
        )
        return f"Command succeeded: {command}\nOutput:\n{result.stdout.strip()}"
    except subprocess.CalledProcessError as e:
        return f"Command failed: {command}\nError:\n{e.stderr.strip()}"


def test_invalid_interface():
    invalid_interface = "eth99"
    print(f"Testing invalid interface: {invalid_interface}")
    commands = [
        f"ip link show {invalid_interface}",
        f"ip link set dev {invalid_interface} up",
        f"ping -I {invalid_interface} -c 3 8.8.8.8",
    ]
    for command in commands:
        output = run_command(command)
        print(output)

    print(f"Finished testing interface: {invalid_interface}")
