# ansible-role-hostname

![GitHub](https://img.shields.io/github/license/jam82/ansible-role-hostname) [![Build Status](https://travis-ci.org/jam82/ansible-role-hostname.svg?branch=main)](https://travis-ci.org/jam82/ansible-role-hostname)

**Ansible role for changing the hostname of a system.**

> WARNING: Use with caution! ;-)

## Purpose

I use this mainly to bootstrap Raspbian installations which have set
`raspberrypi` as default hostname.

I decided to separate [`ansible-role-hosts`](https://github.com/jam82/ansible-role-hosts)
and this one, because I wanted an independant way to manage `/etc/hosts`-entries.

## Supported Platforms

- Alpine
- Amazon
- Archlinux
- CentOS
- Debian
- Fedora
- Manjaro
- OracleLinux
- OpenSuse Leap, Tumbleweed
- Raspbian
- Ubuntu

## Requirements

Ansible 2.9 or higher.

## Variables

Variables and defaults for this role:

```yaml
# The role is disabled by default, so you do not get in trouble.
# Checked in tasks/main.yml.
hostname_role_enabled: false

# If you want to change the hostname of a system, set this.
hostname: "{{ ansible_hostname }}"
```

## Dependencies

Run `ansible-role-hosts` after changing hostname to update your `/etc/hosts`-file

- [`ansible-role-hosts`](https://github.com/jam82/ansible-role-hosts)

This could be a `requirements.yml`-file in your playbook.
See [Ansible Galaxy Docs](https://galaxy.ansible.com/docs/using/installing.html#installing-multiple-roles-from-a-file).

```yaml
---
# file: requirements.yml

- src: https://github.com/jam82/ansible-role-hosts.git
  name: hosts
  version: master
```

## Example Playbooks

Some examples.

### Rename all hosts of a hostgroup

Here is a simple example to rename all hosts of the hostgroup `db`.

> Note: Without updating `/etc/hosts` after changing the hostname,
> I am pretty sure that trouble is ahead.

```yaml
---
# role: ansible-playbook-db
# file: site.yml

- hosts: db
  become: true
  gather_facts: true
  vars:
    hostname_role_enabled: true
    hostname: "db-{{ ansible_hostname }}"
    hosts_role_enabled: true
  roles:
    - role: ansible-role-hostname
    - role: ansible-role-hosts
```

### Configure FQDN with static IP address

Another use case could be, that you want to rename some servers and
all systems should return their FQDN when issuing `hostname -f`.
Some services require this to work, e.g. foreman.

This uses the role
[`ansible-role-hosts`](https://github.com/jam82/ansible-role-hosts)
as dependency and assumes your hosts have static ip addresses.

If the hosts have IP addresses assigned via dhcp as permanent leases
you can add `hosts_ip_static: True` to playbook `vars`.
This prevents the system from getting `127.0.1.1` as IP address in
the `/etc/hosts` file.

The following playbook would update all hostnames of the hostgroup `foreman`
and rewrite the `/etc/hosts`-files with the updated names and IPs.
For the domain name it uses `ansible_domain` implicitly.

If you want to set the domain name explicitly add `hosts_domain: yours.tld`
to the `vars`-dictionary.

```yaml
---
# playbook: ansible-playbook-foreman
# file: site.yml

- hosts: foreman
  become: true
  gather_facts: true
  vars:
    hosts_role_enabled: true
    hostname_role_enabled: true
    hostname: "foreman-{{ ansible_hostname }}"
  roles:
    - role: ansible-role-hostname
    - role: ansible-role-hosts
```

## License and Author

- Author:: [jam82](https://github.com/jam82/)
- Copyright:: 2020, [jam82](https://github.com/jam82/)

Licensed under [MIT License](https://opensource.org/licenses/MIT).
See [LICENSE](https://github.com/jam82/ansible-role-hostname/blob/master/LICENSE) file in repository.

## References

- [ansible.builtin.hostname](https://docs.ansible.com/ansible/latest/collections/ansible/builtin/hostname_module.html)
- [ArchWiki](https://wiki.archlinux.org/)
