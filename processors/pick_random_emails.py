#!/usr/bin/env python

"""Pick an arbitrary number of random emails from the Enron email database"""

import argparse
import errno
import os
from random import randint
import shutil

def get_email_paths(folder_path):
    paths = []
    for email_filename in os.listdir(folder_path):
        path = os.path.join(folder_path, email_filename)
        if os.path.isfile(path):
            paths.append(path)

    return paths

def pick_email(mailbox_paths, email_paths, seen, folder='inbox', max_tries=10000):
    """Pick a random email that hasn't yet been selected"""
    new_email_paths = email_paths.copy()

    for i in range(max_tries):
        mailbox_index = randint(0, len(mailbox_paths) - 1)
        mailbox_path = mailbox_paths[mailbox_index]

        folder_path = os.path.join(mailbox_path, folder)

        if not os.path.exists(folder_path):
            continue

        if folder_path not in new_email_paths:
            new_email_paths[folder_path] = get_email_paths(folder_path)

        email_index = randint(0, len(new_email_paths[folder_path]) - 1)
        email_path = new_email_paths[folder_path][email_index]
        if email_path not in seen:
            newseen = set(seen)
            newseen.add(email_path)
            return email_path, new_email_paths, newseen

    raise Exception("Exhausted all possible emails")

def get_mailbox_paths(maildir):
    """Get a list of paths to individual user mailboxes the individual"""
    paths = []

    for mailbox_dir in os.listdir(maildir):
        path = os.path.join(maildir, mailbox_dir)
        if os.path.isdir(path):
            paths.append(path)

    return paths

def pick_emails(maildir, count):
    """Randomly select a number of emails from the mail directory"""
    seen = set()
    paths = get_mailbox_paths(maildir)
    email_paths = {}

    for i in range(count):
        email_path, email_paths, seen = pick_email(paths, email_paths, seen)
        yield email_path

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description='Pick an arbitrary number of emails from the Enron email dataset.')
    parser.add_argument('maildir',
        help='Directory containing Enron emails')
    parser.add_argument('outputdir',
        help='Directory where the selected emails will be saved')
    parser.add_argument('--count', dest='count', type=int,
        default=1000,
        help='Number of emails to pick')

    args = parser.parse_args()

    try:
        os.makedirs(args.outputdir)
    except OSError as e:
        if e.errno != errno.EEXIST:
            raise

    for i, email_path in enumerate(pick_emails(args.maildir, args.count)):
        dst = os.path.join(args.outputdir, '{0}.txt'.format(i))
        shutil.copyfile(email_path, dst)
