import subprocess

interface = 'eth0'  

def check_connectivity():
    print("Testing network connectivity...")
    try:
        subprocess.run(['ping', '-c', '4', '8.8.8.8'], check=True)
        print("Ping successful! Network connectivity is working.")
        return True
    except subprocess.CalledProcessError:
        print("Ping failed! No network connectivity.")
        return False

def test_check():
    status = check_connectivity()
    assert status == True
