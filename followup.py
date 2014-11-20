#!/usr/bin/env python
#
# Basic script for reminding user to followup on starred (pending)
# emails on an IMAP server
#
# ajclarkson - http://ajclarkson.co.uk

import sys
import imaplib
import email
import email.header
import datetime
import pprint

ACCOUNT_EMAIL = "email"
ACCOUNT_PASS = "password"
FOLLOWUP_FOLDER = "Pending"

account = imaplib.IMAP4_SSL('imap.gmail.com')

def process_mailbox(account):
	status, data = account.search(None, "ALL")
	if status != "OK":
		print "No Messages Found"
		return

	for num in data[0].split():
		status, data = account.fetch(num, '(BODY.PEEK[HEADER.FIELDS (SUBJECT FROM)])')
		header = body = ""
		if status == "OK":
			header = data[0][1]
		else:
			print "ERROR retrieving headers: ", status

		status, data = account.fetch(num, '(BODY.PEEK[TEXT])')
		if status == "OK":
			body = data[0][1]
		else:
			print "ERROR retrieving body: ", status



try:
	status, data = account.login(ACCOUNT_EMAIL, ACCOUNT_PASS)
except imaplib.IMAP4.error:
	print "Login Failed"
	sys.exit(1)

print status, data

status, mailboxes = account.list()

status, data = account.select(FOLLOWUP_FOLDER)
if status == "OK":
	print "Processing Mailbox: %s...\n" % FOLLOWUP_FOLDER
	process_mailbox(account)
	account.close()
else:
	print "ERROR: Unable to open mailbox ", status

account.logout()