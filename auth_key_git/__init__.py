#!/usr/bin/env python3

import ldap
import sys
from os.path import expanduser

ldap_addr = 'ldaps://auth-1.pie.cri.epita.net'
gitolite_user_shell = '/srv/git/bin/gitolite-shell'
dn_group = 'cn=lse, ou=roles, dc=epita, dc=net'

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

        filter = 'objectclass=groupOfNames'
        attrs = ['member']
        results = con.search_s(dn_group, ldap.SCOPE_SUBTREE, filter, attrs)

        users = results[0][1]['member']
        attrs = ['uid', 'sshPublicKey']
        filter = 'objectClass=*'

        for user in users:
          result = con.search_s(user.decode("ascii"), ldap.SCOPE_BASE, filter, attrs)
          for key in result[0][1]['sshPublicKey']:
            print(ssh_options(result[0][1]['uid'][0].decode("ascii"), options), key.strip().decode("ascii"))

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
