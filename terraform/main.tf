data "hetznerdns_zone" "dns_zone" {
  for_each = { for idx, item in var.dns : idx => item }
  name     = each.value.zone
}

resource "hetznerdns_record" "dev" {
  count   = length(var.server)
  zone_id = data.hetznerdns_zone.dns_zone[count.index].id
  name    = var.dns[count.index].subdomain
  value   = digitalocean_droplet.main[count.index].ipv4_address
  type    = "A"
}

#####################

# writing data to files for ansible
resource "github_repository_file" "hosts" {
  repository = var.github.repo
  branch     = "main"
  file       = "./ansible/hosts"
  content = templatefile("inventory.tmpl", {
    servers = var.server
    ips     = digitalocean_droplet.main
  })
  commit_message      = "Add hosts"
  commit_author       = "Terraform User"
  commit_email        = "terraform@example.com"
  overwrite_on_create = true
}



resource "github_repository_file" "group_vars" {
  repository = var.github.repo
  branch     = "main"
  file       = "./ansible/group_vars/group_vars.yml"
  content = templatefile("group_vars.tmpl",
    {
      subdomains = var.dns
    }
  )
  commit_message      = "Add group_vars"
  commit_author       = "Terraform User"
  commit_email        = "terraform@example.com"
  overwrite_on_create = true
}










