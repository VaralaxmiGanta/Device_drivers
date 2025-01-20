import subprocess

# Run iperf3 server as a subprocess
process = subprocess.Popen(
    ["iperf3", "-s"],
    stdout=subprocess.PIPE,   # Capture standard output
    stderr=subprocess.PIPE,   # Capture standard error
    stdin=subprocess.DEVNULL, # No input required
)

print(f"iperf3 server started with PID: {process.pid}")