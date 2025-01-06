import subprocess
import pytest

ASYNC_PATH = "/sys/class/gpio/dummy0/power/async"

def run_command(command, input_data=None):
    try:
        result = subprocess.run(
            command,
            text=True,
            input=input_data,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            check=True,
        )
        return result.stdout.strip()
    except subprocess.CalledProcessError as e:
        pytest.fail(f"Command '{' '.join(command)}' failed: {e.stderr.strip()}")

@pytest.fixture
def setup_gpio_environment():
    # Ensure the `dummy0` device is available before tests
    if not subprocess.run(["test", "-e", ASYNC_PATH], check=False).returncode == 0:
        pytest.skip("GPIO device or async file not found.")
    yield
    # Clean up: Restore default state
    run_command(["sudo", "tee", ASYNC_PATH], input_data="disabled")

def read_async_status():
    return run_command(["sudo", "cat", ASYNC_PATH])
 
def write_async_status(value):
    run_command(["sudo", "tee", ASYNC_PATH], input_data=value)

def test_async_read(setup_gpio_environment):
    status = read_async_status()
    assert status in ["enabled", "disabled"], f"Unexpected async value: {status}"
    print(f"Current async status: {status}")

def test_async_enable(setup_gpio_environment):
    write_async_status("enabled")
    assert read_async_status() == "enabled", "Failed to enable async mode"
    print("Async mode enabled successfully.")


