import os

import pytest

import testinfra.utils.ansible_runner

testinfra_hosts = testinfra.utils.ansible_runner.AnsibleRunner(
    os.environ['MOLECULE_INVENTORY_FILE']).get_hosts('all')


@pytest.fixture
def get_vars(host):
    ansible_facts = host.ansible("setup")
    ansible_distribution = ansible_facts["ansible_facts"]["ansible_distribution"]

    defaults_files = "file=../../defaults/main.yml"
    playbook_vars = "file=../resources/playbooks/vars.yml"
    vars_files = "file=../../vars/" + ansible_distribution + ".yml"

    ansible_vars = host.ansible(
        "include_vars", defaults_files)["ansible_facts"]

    ansible_vars.update(host.ansible(
        "include_vars", playbook_vars)["ansible_facts"])

    ansible_vars.update(host.ansible(
        "include_vars", vars_files)["ansible_facts"])

    return ansible_vars


def test_hostname(host, get_vars):
    short = 'hostname -s'
    output = host.check_output(short)
    assert get_vars['hostname_short'] in output


def test_fqdn(host, get_vars):
    fqdn = 'hostname -f'
    output = host.check_output(fqdn)
    assert get_vars['hostname_fqdn'] in output
