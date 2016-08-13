#!/usr/bin/env python3

import ldap
import sys
from os.path import expanduser

ldap_addr = 'ldaps://auth.pie.cri.epita.net'
gitolite_user_shell = '/srv/git/bin/gitolite-shell'
dn_group = 'ou=lse,ou=labos,dc=epita,dc=net'

def main():
    if len(sys.argv) < 2:
      exit(0)
    username = sys.argv[1]

    try:
      if username == 'git':
        options = [
          'no-port-forwarding',
          'no-X11-forwarding',
          'no-agent-forwarding',
          'no-pty'
        ]

        def command(user):
          return "command=\"%s %s\"" % (gitolite_user_shell, user)

        def ssh_options(user, option):
          return ','.join([command(user)] + option)

        con = ldap.initialize(ldap_addr)
        con.deref = ldap.DEREF_ALWAYS

        filter = 'uid=*'
        attrs = ['uid', 'sshPublicKey']
        users = con.search_s(dn_group, ldap.SCOPE_SUBTREE, filter, attrs)

        for user in users:
          if 'sshPublicKey' in user[1]:
            for key in user[1]['sshPublicKey']:
              print(ssh_options(user[1]['uid'][0].decode("ascii"), options), key.strip().decode("ascii"))

      try:
        # XXX: sanity check missing, username exists
        with open(expanduser('~%s/.ssh/authorized_keys' % username)) as f:
          print(f.read()),
      except:
        pass

    except:
        pass

if __name__ == "__main__":
    main()
