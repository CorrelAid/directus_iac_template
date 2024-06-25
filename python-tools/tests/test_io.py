from ansible_vault import Vault
from python_tools.io import get_yaml_var, get_encrypted_var, get_host

# Test get_yaml_var function
def test_get_yaml_var(tmpdir):
    # Create a temporary YAML file
    yaml_file = tmpdir.join("test.yaml")
    yaml_file.write("var: value")

    # Call the get_yaml_var function with the temporary YAML file
    result = get_yaml_var("var", str(yaml_file))

    # Check if the result is correct
    assert result == "value"

# Test get_encrypted_var function
def test_get_encrypted_var(tmpdir):
    # Create a temporary vault file
    vault_file = tmpdir.join("test.vault")
    vault = Vault("password")
    vault_data = {"var": "value"}
    vault.dump(vault_data, vault_file)

    password_file = tmpdir.join("password_file.txt")
    password_file.write("password")

    # Call the get_encrypted_var function with the temporary vault file
    result = get_encrypted_var("var", str(password_file), str(vault_file))

    # Check if the result is correct
    assert result == "value"

# Test get_host function
def test_get_host(tmpdir):
    # Create a temporary YAML file
    yaml_file = tmpdir.join("test.yaml")
    yaml_file.write("""
[servers]
pink-VP-dev ansible_host=37.27.15.209 ansible_user=deploy_user
pink-VP-prod ansible_host=37.27.16.136 ansible_user=deploy_user
""")

    result = get_host(str(yaml_file), 0)
    assert result == {"host": "37.27.15.209", "user": "deploy_user"}