import paramiko

def execute_on_raspberry_pi(ip_address, username, password, command):
    try:
        # Connect to the Raspberry Pi
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(ip_address, username=username, password=password)

        # Execute a command on the Raspberry Pi
        stdin, stdout, stderr = ssh.exec_command(command)

        # Close the SSH connection
        ssh.close()

        return

    finally:
        ssh.close()