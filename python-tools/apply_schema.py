from python_tools.io import get_host
from python_tools.ssh import create_ssh_client, transfer_folder_via_ssh, run_command_via_ssh

# This script uploads the current local schema and uploads it to the prod server

host = get_host("../ansible/hosts", 1)
hostname = host["host"]
port = 22
username = host["user"]

ssh_client = create_ssh_client(hostname, port, username)

# Transfer a file from the remote server to the local machine
local_path = '../schema-sync'
remote_path = f'/home/{username}/directus/schema-sync'

transfer_folder_via_ssh(ssh_client, local_path, remote_path, direction='put')

run_command_via_ssh(ssh_client, 'docker exec directus npx directus schema-sync import')

# Close the SSH connection
ssh_client.close()