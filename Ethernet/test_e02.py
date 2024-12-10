import subprocess

""" This test case is to verify Ethernet driver correctly loaded and attached to Ethernet device using lspci"""

def verify_ethernet_driver(expected_driver):
    try:
        lspci_output = subprocess.check_output(["lspci", "-k"], text=True)
        lines = lspci_output.splitlines()
        ethernet_device_found = False
        driver_found = False
        actual_driver = None
        ethernet_lines = []

        for i in range(len(lines)):
            if "Ethernet controller" in lines[i]:
                ethernet_device_found = True
                ethernet_lines.append(lines[i])
                print(f"\nDetected Ethernet controller: {lines[i]}")

                for j in range(i + 1, min(i + 4, len(lines))):
                    if "Kernel driver in use" in lines[j]:
                        actual_driver = lines[j].split(":")[-1].strip()
                        print(f"\nActual driver found: {actual_driver}")

                        if actual_driver == expected_driver:
                            driver_found = True
                        break

        if ethernet_lines:
            print("\nFiltered Ethernet Output:")
            for line in ethernet_lines:
                print(line)
        else:
            print("No Ethernet controller found.")

        return ethernet_device_found, driver_found, actual_driver

    except subprocess.CalledProcessError as e:
        print(f"Error executing lspci: {e}")
        return False, False, None

def test_verify_ethernet_driver():
    expected_driver = "e1000"
    ethernet_device_found, driver_found, actual_driver = verify_ethernet_driver(expected_driver)
    assert ethernet_device_found, "No Ethernet controller found in the system."
    assert driver_found, f"Expected driver '{expected_driver}' not found. Actual driver: '{actual_driver}'"
    assert actual_driver == expected_driver, f"Driver mismatch: Expected '{expected_driver}', but found '{actual_driver}'"
    print(f"Assertion passed: Ethernet driver '{actual_driver}' is correctly loaded.")
