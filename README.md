# Ansible Role: hostname

![GitHub](https://img.shields.io/github/license/jomrr/ansible-role-hostname)
![GitHub last commit](https://img.shields.io/github/last-commit/jomrr/ansible-role-hostname)
![GitHub issues](https://img.shields.io/github/issues-raw/jomrr/ansible-role-hostname)
[![dev](https://img.shields.io/github/actions/workflow/status/jomrr/ansible-role-hostname/dev.yml?branch=dev&event=push&label=dev)](https://github.com/jomrr/ansible-role-hostname/actions/workflows/dev.yml?query=branch%3Adev)
[![main](https://img.shields.io/github/actions/workflow/status/jomrr/ansible-role-hostname/main.yml?branch=main&event=push&label=main)](https://github.com/jomrr/ansible-role-hostname/actions/workflows/main.yml?query=branch%3Amain)

Ansible role for managing the system hostname.

## Purpose

Install hostname utilities and set the system hostname on physical machines
and virtual machines. Container guests, including Docker, Podman, and LXC,
retain the hostname
assigned by their container runtime.

## Scope

### Managed

- Platform-specific hostname utility packages.
- The active and persistent system hostname on supported non-container hosts.

### Not Managed

- Container runtime configuration and container hostnames.
- DNS records, resolver configuration, and /etc/hosts entries.

## Requirements

- Gather Ansible facts before applying the role.

## Dependencies

```yaml
collections:
  - name: community.general
    version: '>=12.0.0'
```

## Role Variables

### `hostname_name`

Type: `str`. Required: `false`.

Desired system hostname; a short name without dots is recommended.
Defaults to the current short hostname.
Hostname changes are skipped in containers, including Docker, Podman, and LXC.

Default:

```yaml
hostname_name: '{{ ansible_facts.hostname }}'
```

## Check Mode

Package and hostname changes support Ansible check mode without applying
changes.

- The container exclusion also applies in check mode.

## Service Behavior

The hostname module applies changes directly; no services are restarted.

## Operational Notes

- Idempotent: subsequent runs with the same desired hostname and installed
  packages report no changes.
- A short hostname with a single DNS label is recommended. The default uses
  ansible_facts.hostname, so an existing FQDN is shortened on non-container
  hosts. An explicitly configured hostname_name is passed to the hostname module
  unchanged.
- Migration: replace the former hostname variable with hostname_name.
- Molecule checks utility availability, idempotency, check mode, and
  preservation of the runtime-assigned container hostname despite a different
  requested name. Hostname changes on physical machines and virtual machines
  require separate validation outside the container scenarios.

## Supported Platforms

| OS Family | Distribution | Version | Container Image |
| --------- | ------------ | ------- | --------------- |
| RedHat | AlmaLinux | latest | [jomrr/molecule-almalinux:latest](https://hub.docker.com/r/jomrr/molecule-almalinux) |
| Debian | Debian | latest | [jomrr/molecule-debian:latest](https://hub.docker.com/r/jomrr/molecule-debian) |
| RedHat | Fedora | latest | [jomrr/molecule-fedora:latest](https://hub.docker.com/r/jomrr/molecule-fedora) |
| Suse | OpenSuse Leap | latest | [jomrr/molecule-opensuse-leap:latest](https://hub.docker.com/r/jomrr/molecule-opensuse-leap) |
| Suse | OpenSuse Tumbleweed | latest | [jomrr/molecule-opensuse-tumbleweed:latest](https://hub.docker.com/r/jomrr/molecule-opensuse-tumbleweed) |
| Debian | Ubuntu | latest | [jomrr/molecule-ubuntu:latest](https://hub.docker.com/r/jomrr/molecule-ubuntu) |

## Example Playbook

### Set a short hostname

Configure a short hostname on physical machines and virtual machines.

```yaml
---
# name: "jomrr.hostname"
# file: "playbook_hostname.yml"

- name: "PLAYBOOK | hostname"
  hosts: "hostname_hosts"
  gather_facts: true
  roles:
    - role: "jomrr.hostname"
      hostname_name: "web01"
```

## References

- [Systemd hostname recommendations](https://github.com/systemd/systemd/blob/main/man/hostname.xml)
- [Ansible hostname module](https://docs.ansible.com/projects/ansible/latest/collections/ansible/builtin/hostname_module.html)

## Author

[Jonas Mauer](https://github.com/jomrr)

## License

This project is licensed under the MIT License.
See [LICENSE](LICENSE) for the full license text.

Copyright (c) 2020 Jonas Mauer.
