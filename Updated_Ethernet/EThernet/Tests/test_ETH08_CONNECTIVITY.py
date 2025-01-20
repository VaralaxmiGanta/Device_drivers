import subprocess

"This test case is to check the Network Connectivity by pining the ip"

def check_connectivity():
    try:
        subprocess.run(['sudo','ping', '-c', '4', '8.8.8.8'], check=True)
        print("Ping successful! Network connectivity is working.")
        return True
    except subprocess.CalledProcessError:
        print("Ping failed! No network connectivity.")
        return False

def test_check():
    status = check_connectivity()
    assert status == True
    print("Network Connectivity test passed")
