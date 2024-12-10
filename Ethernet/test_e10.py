import subprocess


def run_iperf(client_ip, packet_size, window_size):
    try:
        result = subprocess.run(
            ["iperf", "-c", client_ip, "-l", packet_size, "-w", window_size],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        output = result.stdout
        if result.returncode != 0:
            print(f"Error: {result.stderr}")
            return None

        for line in output.split("\n"):
            if "Mbits/sec" in line:
                return line.strip()

        return "Throughput not found in output."
    except Exception as e:
        print(f"An error occurred: {e}")
        return None


def main():
    server_ip = "172.17.17.93"

    packet_sizes = ["512", "1K", "8K"]
    window_sizes = ["64K", "128K", "256K"]

    results = []
    for packet_size in packet_sizes:
        for window_size in window_sizes:
            print(f"Testing with Packet Size: {packet_size}, Window Size: {window_size}")
            throughput = run_iperf(server_ip, packet_size, window_size)
            results.append((packet_size, window_size, throughput))

    print("\nTest Results:")
    print(f"{'Packet Size':<15} {'Window Size':<15} {'Throughput':<30}")
    print("-" * 60)
    for packet_size, window_size, throughput in results:
        print(f"{packet_size:<15} {window_size:<15} {throughput:<30}")


if __name__ == "__main__":
    main()
