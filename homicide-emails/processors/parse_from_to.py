#!/usr/bin/env python

# Parse `From:`, `To:` and `Cc:` headers from an email and output as JSON.
# Usage: parse_from_to.py email_file.txt

import argparse
import email
import json
import sys

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('infile', nargs='?', type=argparse.FileType('r'),
                        default=sys.stdin)
    args = parser.parse_args()
    msg = email.message_from_file(args.infile)

    print(json.dumps({
        'id':  msg.get('message-id'),
        'from': msg.get('from'),
        # email.utils.getaddresses returns pairs of names and email addresses.
        # We just care about the addresses
        'to': [a[1] for a in email.utils.getaddresses(msg.get_all('to', []))],
        'cc': [a[1] for a in email.utils.getaddresses(msg.get_all('cc', []))],
    }))
