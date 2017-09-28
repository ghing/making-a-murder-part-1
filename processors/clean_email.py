#!/usr/bin/env python

import sys

def replace_email_domain(s):
    return s.replace("@enron.com", "@tcpolice.org")


if __name__ == "__main__":
    transforms = [
      replace_email_domain,
    ]

    email_text = sys.stdin.read()

    for fn in transforms:
        email_text = fn(email_text)

    sys.stdout.write(email_text)
