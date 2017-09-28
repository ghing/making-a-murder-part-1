#!/usr/bin/env python

# Process a newline-delimited JSON file of from/to/cc information about emails
# to get a count of how often each email account emailed other email accounts.
# 
# That is, go from data like this:
#
#     { "from": "email1@example.com", "to": ["email2@example.com"], "cc": [] }
#     { "from": "email1@example.com", "to": ["email3@example.com"], "cc": ["email2@example.com"] }
#    
# To data like this: 
# 
# {
#   "emai1@example.com" : {
#     "email2@example.com": 2,
#     "email3@example.com": 1
#   }
# }
#
# Usage: count_connections.py < email_to_from.ndjson

import json
import sys

if __name__ == "__main__":
    senders = {}

    for line in sys.stdin:
        email_data = json.loads(line)

        recipients = senders.setdefault(email_data['from'], {})
        for addr in email_data['to'] + email_data['cc']:
            if addr not in recipients:
                recipients[addr] = 0

            recipients[addr] += 1

    print(json.dumps(senders))
