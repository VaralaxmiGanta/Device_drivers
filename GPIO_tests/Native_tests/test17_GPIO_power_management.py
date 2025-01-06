import os
import subprocess
import pytest

# Paths to the power management files
POWER_DIR = "/sys/class/gpio/dummy0/power"
FILES = {
    "runtime_status": "runtime_status",
    "runtime_active_time": "runtime_active_time",
    "runtime_suspended_time": "runtime_suspended_time",
    "runtime_usage": "runtime_usage",
    "runtime_enabled": "runtime_enabled",
}

@pytest.fixture(scope="function")
def check_power_files():
    missing_files = [f for f in FILES.values() if not os.path.exists(os.path.join(POWER_DIR, f))]
    if missing_files:
        pytest.skip(f"Missing files: {', '.join(missing_files)}. Skipping test.")

def test_power_files_exist():
    for file_name in FILES.values():
        file_path = os.path.join(POWER_DIR, file_name)
        assert os.path.exists(file_path), f"{file_name} does not exist"

@pytest.mark.parametrize("file_name", FILES.keys())
def test_read_power_file(file_name, check_power_files):
    file_path = os.path.join(POWER_DIR, FILES[file_name])
    try:
        with open(file_path, "r") as f:
            content = f.read().strip()
        print(f"Content of {file_name}: {content}")
        assert content is not None, f"{file_name} returned no content"
    except Exception as e:
        pytest.fail(f"Failed to read {file_name}: {e}")

if __name__ == "__main__":
    pytest.main(["-s", __file__])

