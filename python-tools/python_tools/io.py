import yaml
import configparser
from ansible_vault import Vault

def get_yaml_var(var,file_path):
    with open(file_path, 'r') as stream:
        data = yaml.safe_load(stream)
    var = data[var]
    return var

def get_encrypted_var(var, vault_password_file_path, vault_file_path, index=None):
    with open(vault_password_file_path, 'r') as stream:
        vault_password = stream.read()
    vault = Vault(password=vault_password)
    vault_data = vault.load(open(vault_file_path, 'r').read())
    var = vault_data[var]
    if index is not None:
        var = var[index]
    return var

def get_host(file_path, i):
    config = configparser.ConfigParser()
    config.read(file_path)

    servers = dict(config.items('servers'))  # Get all the items in the 'servers' section as a dictionary
    servers_details = {key: value for key, value in servers.items()}  # Convert the items to a regular dictionary
    servers = list(servers.keys())

    key = servers[i].strip()
    server_host = servers_details[key].split(' ')[0]
    server_user = servers_details[key].split(' ')[1].split('=')[1]

    return {"host": server_host, "user": server_user}