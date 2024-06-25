from python_tools.directus_auth import Directus
from python_tools.helpers import dev_admin_mail, dev_admin_pw, dev_base_url
import requests


def test_get_access_token():
   
    directus = Directus(dev_admin_mail(), dev_admin_pw(), dev_base_url())

    access_token = directus.get_access_token()

    assert isinstance(access_token, str)
    
    url = f"{dev_base_url()}/server/info"
    response = requests.get(url)
    
    assert response.status_code == 200, f"Request failed with status code: {response.status_code}"
    data = response.json().get("data")
    assert isinstance(data, dict)
    assert "project" in list(data)
       