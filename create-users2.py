#!/usr/bin/python3
# INET 4031 - Automated user creation w/ dry-run
# Author: Payton Gagne

import os
import re
import sys

def main():
    # ask user if dry run
    dry_run = input("Run in dry-run mode? (Y/N): ").strip().lower() == 'y'

    for line in sys.stdin:
        # skip comment lines
        if re.match(r"^#", line):
            if dry_run:
                print("Skipped comment line.")
            continue

        # split fields and check count
        fields = line.strip().split(':')
        if len(fields) != 5:
            if dry_run:
                print("Invalid line skipped:", line.strip())
            continue

        # map fields
        username = fields[0]
        password = fields[1]
        gecos = "%s %s,,," % (fields[3], fields[2])
        groups = fields[4].split(',')

        print("==> Creating account for %s..." % username)
        cmd = "/usr/sbin/adduser --disabled-password --gecos '%s' %s" % (gecos, username)
        if dry_run:
            print("[DRY-RUN] Would run:", cmd)
        else:
            os.system(cmd)

        print("==> Setting password for %s..." % username)
        cmd = "/bin/echo -ne '%s\n%s' | /usr/bin/sudo /usr/bin/passwd %s" % (password, password, username)
        if dry_run:
            print("[DRY-RUN] Would run:", cmd)
        else:
            os.system(cmd)

        for group in groups:
            if group != '-':
                print("==> Assigning %s to %s..." % (username, group))
                cmd = "/usr/sbin/adduser %s %s" % (username, group)
                if dry_run:
                    print("[DRY-RUN] Would run:", cmd)
                else:
                    os.system(cmd)

if __name__ == "__main__":
    main()
