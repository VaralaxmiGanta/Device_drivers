import subprocess


def check_driver_using_lsmod(driver_name):
    try:
        lsmod_output = subprocess.check_output(["lsmod"], text=True)
        if driver_name in lsmod_output:
            print(f"Driver '{driver_name}' is loaded (from lsmod).")
            return True
        else:
            print(f"Driver '{driver_name}' is NOT loaded (from lsmod).")
            return False
    except subprocess.CalledProcessError as e:
        print(f"Error executing 'lsmod': {e}")
        return False


def check_driver_using_lspci(driver_name):
    try:
        lspci_output = subprocess.check_output(["lspci", "-k"], text=True)
        if driver_name.lower() in lspci_output.lower():
            print(f"Driver '{driver_name}' is associated with an Ethernet device (from lspci -k).")
            return True
        else:
            print(f"Driver '{driver_name}' is NOT associated with an Ethernet device (from lspci -k).")
            return False
    except subprocess.CalledProcessError as e:
        print(f"Error executing 'lspci -k': {e}")
        return False


def check_ethernet_driver(driver_name):

    # Check using lsmod
    lsmod_check = check_driver_using_lsmod(driver_name)

    # Check using lspci -k
    lspci_check = check_driver_using_lspci(driver_name)

    if lsmod_check and lspci_check:
        print(f"Driver '{driver_name}' is loaded and associated with an Ethernet device.")
    else:
        print(f"Driver '{driver_name}' is not properly loaded or associated with an Ethernet device.")


if __name__ == "__main__":
    driver_name = "e1000e"
    check_ethernet_driver(driver_name)
