#!/usr/bin/env python3

import configparser
import ldap
import os
import sys
from os.path import expanduser


def load_config():
    defaults = {
        'shell': '/usr/lib/gitolite/gitolite-shell',
        'options': 'no-port-forwarding,no-X11-forwarding,no-agent-forwarding,no-pty',
        'user': 'git',
    }
    config_files = [
        '/etc/authkeygit/authkeygitrc',
        expanduser('~/.authkeygitrc'),
        'authkeygitrc',
    ]
    conf = configparser.SafeConfigParser(defaults)
    conf.add_section('git')
    conf.add_section('ldap')
    conf.read(config_files)
    return conf

def main():
    if len(sys.argv) < 2:
        exit(0)
    username = sys.argv[1]

    config = load_config()
    if username != config.get('git', 'user'):
        exit(0)

    try:
        with open(expanduser('~%s/.ssh/authorized_keys' % username)) as f:
            print(f.read())
    except:
        pass

    def command(user):
        return "command=\"%s %s\"" % (config.get('git', 'shell'), user)

    def ssh_options(user, option):
        return '{},{}'.format(command(user), option)

    try:
        con = ldap.initialize(config.get('ldap', 'ldap_addr'))
        con.deref = ldap.DEREF_ALWAYS

        attrs = config.get('ldap', 'attrs').split(",")
        users = con.search_s(config.get('ldap', 'dn_group'),
                           ldap.SCOPE_SUBTREE,
                           config.get('ldap', 'filter'),
                           attrs)

        for user in users:
            if 'sshPublicKey' in user[1]:
                for key in user[1]['sshPublicKey']:
                    options = ssh_options(user[1]['uid'][0].decode("ascii"), config.get('git', 'options'))
                    print(options, key.strip().decode("ascii"))
    except:
        pass


if __name__ == "__main__":
    main()
