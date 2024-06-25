# Directus Template


## Setup

1. Install Requirements
- [Copier](https://copier.readthedocs.io/en/stable/#installation)
    - install at least copier=v9.2.0
- [Ansible](https://docs.ansible.com/ansible/latest/installation_guide/intro_installation.html#installing-and-upgrading-ansible)
- [Terraform](https://developer.hashicorp.com/terraform/tutorials/aws-get-started/install-cli)
- [Pre-commit](https://pre-commit.com/#installation)
- [Poetry](https://python-poetry.org/docs/#installation)

2. Retrieve input data file 

`curl -o input.yml https://raw.githubusercontent.com/CorrelAid/directus_iac_template/main/input.yml.tmpl`

3. Edit values of input data file

See the file itself. Sensitive data will be stored in ansible vault and will not be stored in the answers.yml of copier. Be aware however, that they are still hardcoded in the input data file you edited. Best practice is to delete this file after you are done.

4. Run copier

`copier copy --data-file input.yml --trust gh:CorrelAid/directus_iac_template <folder name>`

5. cd into the resulting folder and set up pre-commit

```
git init
pre-commit install
```

6. Create Repo in browser **with name specified in input data**, then and commit local files to new repo 

```
git add .
git commit -m "init"
git remote add origin git@github.com:CorrelAid/<repo name>.git
git branch -M main
git push -u origin main
```

7. Provide Terraform with the required tokens

Depends on how you run terraform. If your run it locally, set the environment variables:

```
# depends on which provider you chose
# export DIGITALOCEAN_TOKEN=token 
export HCLOUD_TOKEN=token
export HETZNER_DNS_API_TOKEN=token
export GITHUB_TOKEN=token
```

8. cd into /terraform folder and tun terraform

```
terraform init
terraform apply
```

9. Pull changes made through terraform

10. cd to root folder and run ansible

```
ansible-playbook ansible/playbook.yml
```

11. cd into /python-tools and install poetry project

`poetry install`

## Functionality

The python-tools package contained in this folder provides some functionality to interact with the directus instances

### Save schema on dev server

`poetry run python save_schema.py`

### Save schema on prod server

`poetry run python apply_schema.py`

