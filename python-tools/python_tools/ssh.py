import paramiko
import os
import stat


def create_ssh_client(hostname, port, username):
    """
    Create an SSH client using an SSH key for authentication, and return the client object.
    Prompt for the SSH key path with a default option.
    """
    # get current username
    user= os.getlogin()
    default_ssh_key_path=f'/home/{user}/.ssh/id_rsa'

    ssh_client = paramiko.SSHClient()
    ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    
    ssh_key_path = input(
        f"Enter the path to the SSH key file (press Enter to use the default '{default_ssh_key_path}'): ")
    if not ssh_key_path:
        ssh_key_path = default_ssh_key_path
    
    private_key = paramiko.RSAKey.from_private_key_file(ssh_key_path)
    print(hostname, port, username)
    ssh_client.connect(hostname, port, username, pkey=private_key)
    return ssh_client

def transfer_folder_via_ssh(ssh_client, local_folder, remote_folder, direction='put'):
    """
    Transfer a folder via SSH using the provided SSH client.
    Set direction to 'put' for transferring from local to remote,
    or 'get' for transferring from remote to local.
    """
    sftp_client = ssh_client.open_sftp()
    if direction == 'put':
        for root, dirs, files in os.walk(local_folder):
            remote_root = os.path.join(remote_folder, os.path.relpath(root, local_folder))
            # Create remote subdirectories if they do not exist
            for dir in dirs:
                remote_dir = os.path.join(remote_root, dir)
                try:
                    sftp_client.stat(remote_dir)
                except IOError:
                    sftp_client.mkdir(remote_dir)
            for file in files:
                local_path = os.path.join(root, file)
                remote_path = os.path.join(remote_root, file)
                sftp_client.put(local_path, remote_path)
    elif direction == 'get':
        def get_recursive(remote_dir, local_dir):
            for item in sftp_client.listdir_attr(remote_dir):
                remote_path = remote_dir + '/' + item.filename
                local_path = os.path.join(local_dir, item.filename)
                if stat.S_ISDIR(item.st_mode):
                    os.makedirs(local_path, exist_ok=True)
                    get_recursive(remote_path, local_path)
                else:
                    sftp_client.get(remote_path, local_path)
        get_recursive(remote_folder, local_folder)
    else:
        raise ValueError(
            "Invalid direction. Use 'put' for transferring from local to remote, or 'get' for \
                transferring from remote to local.")
    sftp_client.close()

def run_command_via_ssh(ssh_client, command):
    """
    Run a command via SSH using the provided SSH client.
    """
    stdin, stdout, stderr = ssh_client.exec_command(command)
    
    # Capture and print command output
    stdout_lines = stdout.readlines()
    stderr_lines = stderr.readlines()
    
    for line in stdout_lines:
        print(line, end="")
    
    for line in stderr_lines:
        print(line, end="")
    
    return stdout_lines, stderr_lines
