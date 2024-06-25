# Directus Template


## Setup

1. Install Requirements
- [Copier](https://copier.readthedocs.io/en/stable/#installation)
    - install at least copier=v9.2.0
- [Ansible](https://docs.ansible.com/ansible/latest/installation_guide/intro_installation.html#installing-and-upgrading-ansible)
- 

2. Retrieve input data file 

`curl -o input.yml https://raw.githubusercontent.com/CorrelAid/directus_iac_template/main/input.yml.tmpl`

3. Edit values of input data file



5. Provide Terraform with the required tokens
```
# export DIGITALOCEAN_TOKEN=token 
expprt HCLOUD_TOKEN=token
export HETZNER_DNS_API_TOKEN=token
export GITHUB_TOKEN=token
```