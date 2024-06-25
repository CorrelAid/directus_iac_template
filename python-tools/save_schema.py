from python_tools.io import get_host
from python_tools.ssh import create_ssh_client, transfer_folder_via_ssh

# This script downloads the schema from the development server and saves it locally to be committed to github

host = get_host("../ansible/hosts", 0)
hostname = host["host"]
port = 22
username = host["user"]
ssh_client = create_ssh_client(hostname, port, username)

# Transfer a file from the remote server to the local machine
local_path = '../schema-sync'
remote_path = f'/home/{username}/directus/schema-sync'

transfer_folder_via_ssh(ssh_client, local_path, remote_path, direction='get')

# Close the SSH connection
ssh_client.close()