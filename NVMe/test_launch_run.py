import paramiko
import time
import subprocess


def is_vm_running(host, port, username, password):
    try:
        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        client.connect(host, port=port, username=username, password=password)
        client.close()
        return True
    except Exception:
        return False


def launch_qemu():
    qemu_command = [
        "qemu-system-riscv64",
        "-machine", "virt",
        "-cpu", "rv64",
        "-m", "8G",
        "-device", "nvme,drive=nvme0,serial=1234",
        "-drive", "file=nvme.qcow2,if=none,id=nvme0",
        "-device", "virtio-net-device,netdev=net",
        "-netdev", "user,id=net,hostfwd=tcp::2222-:22",
        "-device", "virtio-blk-pci,drive=hd",
        "-drive", "file=/home/vlab/veena/dqib_riscv64-virt/image.qcow2,if=none,id=hd",
        "-bios", "/usr/lib/riscv64-linux-gnu/opensbi/generic/fw_jump.elf",
        "-kernel", "/usr/lib/u-boot/qemu-riscv64_smode/uboot.elf",
        "-serial", "mon:stdio",
        "-nographic"
    ]
    subprocess.Popen(qemu_command)
    print("QEMU VM is booting...")


def wait_for_ssh(host, port, username, password, timeout=300, interval=10):
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    start_time = time.time()

    while time.time() - start_time < timeout:
        try:
            print("Trying to connect to the VM via SSH...")
            client.connect(host, port=port, username=username, password=password)
            print("Connected to the VM.")
            client.close()
            return True
        except (paramiko.SSHException, ConnectionResetError):
            print(f"SSH not available yet, retrying in {interval} seconds...")
            time.sleep(interval)

    print("Timeout reached, SSH connection failed.")
    return False


def run_remote_script(host, port, username, password, script_path):
    try:
        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        client.connect(host, port=port, username=username, password=password)

        # Run the test script
        print(f"running {script_path}")
        stdin, stdout, stderr = client.exec_command(f"sudo pytest -v -s {script_path}")
        output = stdout.read().decode()
        errors = stderr.read().decode()

        print("Output:\n", output)
        if errors:
            print("Errors:\n", errors)

        client.close()
    except Exception as e:
        print(f"An error occurred while running the script: {e}")


def main():
    host = "localhost"
    port = 2222
    username = "debian"
    password = "debian"
    script_paths = [
        "~/NVme/test_c01.py",
        "~/NVme/test_c02.py",
        "~/NVme/test_c03.py",
        "~/NVme/test_c04.py",
        "~/NVme/test_c05.py",
        "~/NVme/test_c06.py",
        "~/NVme/test_c07.py",
        "~/NVme/test_c08.py",
        "~/NVme/test_c09.py",
        "~/NVme/test_c10.py",
        "~/NVme/test_c11.py",
        "~/NVme/test_c12.py",
        "~/NVme/test_c13.py",
        "~/NVme/test_c14.py",

    ]

    if not is_vm_running(host, port, username, password):
        print("VM is not running. Launching VM...")
        launch_qemu()

        if wait_for_ssh(host, port, username, password):
            print("VM is ready. Running the test scripts...")
            for script in script_paths:
                run_remote_script(host, port, username, password, script)
        else:
            print("Failed to connect to the VM after retries.")
    else:
        print("VM is already running. Running the test scripts...")
        for script in script_paths:
            run_remote_script(host, port, username, password, script)


if __name__ == "__main__":
    main()
