import subprocess


"This test case is to verify that the driver is properly handling network packets and allowing communication with a domain name, via the IP address resolved by DNS."

def check_connectivity():
    try:
        subprocess.run(['sudo','ping', '-c', '4', 'google.com'], check=True)
        print("Ping successful! Network connectivity is working.")
        return True
    except subprocess.CalledProcessError:
        print("Ping failed! No network connectivity.")
        return False

def test_check():
    status = check_connectivity()
    assert status == True
    print("Network Connectivity test passed")

