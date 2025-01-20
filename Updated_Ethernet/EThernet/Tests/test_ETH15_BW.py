import subprocess 

"THis test case is to verify the bandwidth"
#before running this setup the server also using iperf -s 

def test_bandwidth():
    server_ip = "172.17.17.14"
    result = subprocess.run(["iperf", "-c", server_ip], capture_output=True, text=True)
    for line in result.stdout.splitlines():
       if "Mbits/sec" in line:
          print("\nBandwidth : ",line.strip())
    assert result.returncode == 0, f"Bandwidth test to {server_ip} failed"
    assert "Mbits/sec" in result.stdout, "Bandwidth result not found"
