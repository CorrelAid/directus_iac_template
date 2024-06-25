from datetime import datetime, timedelta
import requests

def get_data(response):
    data = response.json().get("data")
    access_token = data["access_token"]
    refresh_token = data["refresh_token"]
    expires = data["expires"]
    expire_time = datetime.now() + timedelta(milliseconds=expires)
    return access_token,refresh_token,expire_time


def login(admin_mail, admin_pw, base_url):
    url = f"{base_url}/auth/login"
    data = {
        "email": admin_mail,
        "password": admin_pw,
    }
    response = requests.post(url, json=data)
    return get_data(response)

def refresh_access_token(refresh_token,base_url):
    url = f"{base_url}/auth/refresh"
    data = {
        "refresh_token": refresh_token,
        "mode": "json"
    }

    response = requests.post(url, json=data)
    return get_data(response)


class Directus:
    def __init__(self, admin_mail, admin_pw, base_url):
        self.base_url = base_url
        self.admin_mail = admin_mail
        self.admin_pw = admin_pw
        self.access_token, self.refresh_token, self.expire_time = login(admin_mail, admin_pw, base_url)
    
    def get_access_token(self):
        if datetime.now() > self.expire_time:
            self.access_token, self.refresh_token, self.expire_time = refresh_access_token(self.refresh_token, 
                                                                                           self.base_url)
        return self.access_token




