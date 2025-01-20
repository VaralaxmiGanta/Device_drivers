import subprocess
import time

"""THis test case is to verify the latency"""

def ping(target_ip="8.8.8.8", count=10):
    print(f"Pinging {target_ip} to measure latency...")
    try:
        result = subprocess.run(["ping", "-c", str(count), target_ip], capture_output=True, text=True, check=True)
        output = result.stdout
        print(output)

        avg_latency = None
        for line in output.splitlines():
            if "avg" in line:
                avg_latency = line.split("=")[-1].strip().split("/")[1]
                break

        if avg_latency:
            print(f"Average latency: {avg_latency} ms")
            return float(avg_latency)
        else:
            print("Unable to parse latency from ping output.")

    except subprocess.CalledProcessError as e:
        print(f"Ping failed: {e}")

def test_ping():
       measured_lat = ping()
       assert measured_lat  <= 18.0
