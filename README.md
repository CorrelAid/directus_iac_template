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

See the file itself. Sensitive data will be stored in ansible vault and will not be stored in the answers.yml of copier. Be aware however, that they are still hardcoded in the input data file you edited. Best practice is to delete this file after you are done.

4. Run copier

`copier copy --data-file input.yml --trust directus_iac_template testcopier copy --data-file input.yml --trust directus_iac_template <folder path>`

4. Provide Terraform with the required tokens
Depends on how you run terraform. If your run it locally, set the environment variables:

```
# depends on which provider you chose
# export DIGITALOCEAN_TOKEN=token 
export HCLOUD_TOKEN=token
export HETZNER_DNS_API_TOKEN=token
export GITHUB_TOKEN=token
```

