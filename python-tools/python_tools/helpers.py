import json
import requests
from datetime import datetime
from python_tools.io import get_yaml_var, get_encrypted_var
from python_tools.directus_auth import Directus
from python_tools.models.main import Lumpinbreast, Scan, Screening


vault_password_file_path = "../ansible/.vault_pw"
vault_file_path = "../ansible/group_vars/vault.yml"

def dev_admin_mail():
    return get_encrypted_var("directus_admin_mail", vault_password_file_path, vault_file_path)[0]

def dev_admin_pw():
    return get_encrypted_var("directus_admin_pw", vault_password_file_path, vault_file_path)[0]

def dev_base_url():
    return f'https://{get_yaml_var("subdomain", "../ansible/group_vars/group_vars.yml")[0]}'

def dev_mail():
    return get_encrypted_var("smtp_user", vault_password_file_path, vault_file_path)[0]


def role_ids(role_name):
    with open("../schema-sync/data/directus_roles.json", "r") as f:
        roles = json.load(f)
    for role in roles:
       if role["name"] == role_name:
           return role["id"]

def get_folder_id(folder_name):
    with open("../schema-sync/data/directus_folders.json", "r") as f:
        folders = json.load(f)
    for folder in folders:
        if folder["name"] == folder_name:
            return folder["id"]


def admin_role_id():
    headers = { "Authorization": f"Bearer {dev_admin_access_token()}" }
    url = f"{dev_base_url()}/users/me"
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    return response.json()["data"]["role"]

        
def dev_admin_access_token():
    directus = Directus(dev_admin_mail(), dev_admin_pw(), dev_base_url())
    access_token = directus.get_access_token()
    return access_token

def create_user(email, password, role_id, name: str, access_token = None):
    url = f"{dev_base_url()}/users"
    user_object = {
        "email":    email,
        "password": password,
        "role": role_id,
        "name": name
    }
    if access_token is not None:
        headers = { "Authorization": f"Bearer {access_token}" }
        response = requests.post(url, headers=headers, json=user_object)
        response.raise_for_status()
    else:
        response = requests.post(url, json=user_object)
        print(response.text)
        response.raise_for_status()
    
    directus = Directus(email, password, dev_base_url())

    access_token = directus.get_access_token()

    url = f"{dev_base_url()}/users/me"
    headers = { "Authorization": f"Bearer {access_token}" }
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    user_object = response.json()
    if ("id" not in user_object["data"]):
        user_id = user_object["data"]
    else:

        user_id = user_object["data"]["id"]

    return {"access_token": access_token, "email": email, "password": password, 
        "id": user_id}

def create_entry(Collection: str, data: dict, access_token: str):
    url = f"{dev_base_url()}/items/{Collection}"
    headers = { "Authorization": f"Bearer {access_token}" }
    response = requests.post(url, headers=headers, json=data)
    return response


def get_flow_id(name: str, access_token: str):
    url = f"{dev_base_url()}/flows/"
    headers = { "Authorization": f"Bearer {access_token}" }
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    for flow in response.json()["data"]:
        if flow["name"] == name:
            return flow["id"]
    raise Exception(f"Flow {name} not found")

def get_trigger_id(flow_id: str, access_token: str):
    url = f"{dev_base_url()}/flows/{flow_id}"
    headers = { "Authorization": f"Bearer {access_token}" }
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    return response.json()["data"]["operation"]

def change_trigger_cron(flow_id: str, cron: str, access_token: str):
    url = f"{dev_base_url()}/flows/{flow_id}"
    headers = { "Authorization": f"Bearer {access_token}" }
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    jason = response.json() 
    current_cron = jason["data"]["options"]["cron"]
    if current_cron != cron:
        response = requests.patch(url, headers=headers, json={"options": {"cron": cron}})
        response.raise_for_status()
    return current_cron

def switch_flow(flow_id: str, access_token: str, status: str = "active"):
    url = f"{dev_base_url()}/flows/"
    headers = { "Authorization": f"Bearer {access_token}" }
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    url = f"{dev_base_url()}/flows/{flow_id}"
    # check if flow is active
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    current_status = response.json()["data"]["status"]
    if current_status != status:
        response = requests.patch(url, headers=headers, json={"status": status})
        response.raise_for_status()
    return current_status


