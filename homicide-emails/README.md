# homicide emails

Extract emails from PDF printout of emails obtained from TCPD leak.

I want to do look at the connections between email senders and recipients.  See if I can find outliers.  Maybe use the data to do some kind of network viz whenever (if haha) we publish.

TODO: I wrote some python scripts that I think will get the relevent sender/recipient info out of a text email, and something that will count everything up.  I need to figure out how to run that on all the emails.  I heard someone talk about using make at a conference so I'm gonna try that.

## What's in here

* `processors/parse_from_to.py` - Python script to extract sender and recipients from the text of a single email
* `processors/count_connections.py` - Python script to take the output of the `parse_from_to.py` script and count how many times each person emailed another address.
* `cheatsheet.md` - Copy of my notes from the command line for journalism session at NICAR a few years ago.

## Assumptions

* The `pdftotext` program.  If you're on a mac with homebrew, you can install it with `brew install poppler`.
* make. You probably already have this if you've installed Homebrew or the OS X developer tools

## Extract the emails

Just run `make`.
