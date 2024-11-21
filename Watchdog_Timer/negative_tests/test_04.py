"""
Test writing to the watchdog when it is disabled.
Run this test case with --noconftest option while using pytest 
It will give Device not found
"""
import pytest
import os

WATCHDOG_DEVICE_PATH = "/dev/watchdog"

def test_write_to_disabled_watchdog():
    # Check if the device exists
    if not os.path.exists(WATCHDOG_DEVICE_PATH):
        print(f"Watchdog device not found at {WATCHDOG_DEVICE_PATH}")
        return

