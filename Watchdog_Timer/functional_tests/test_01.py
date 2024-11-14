"""Check if the watchdog kernel module is loaded."""

import os
import subprocess
import pytest


def test_watchdog_kernel_module():
    try:
        result = subprocess.run(
            ['lsmod', '|', 'grep', 'watchdog'],
            check=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )
        assert 'watchdog' in result.stdout.decode(), "Watchdog kernel module is not loaded."
    except subprocess.CalledProcessError:
        pytest.fail("Watchdog kernel module is not loaded.")
