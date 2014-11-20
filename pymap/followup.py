
class ReplyReminder:
	def __init__(self, mail_account, followup_folder):
		self.status, data = mail_account.imap.select(followup_folder)

	def process_mailbox(self, mail_account, followup_folder):
		mail_account.imap.select(followup_folder)
		status, data = mail_account.imap.search(None, "ALL")
		if status != "OK":
			print "No messages found in %s:%s" % (mail_account.name, followup_folder)
			return

		pending_messages = []
		for num in data[0].split():
			header = self.fetch_message_part(mail_account, num, '(BODY.PEEK[HEADER.FIELDS (SUBJECT FROM)])')
			body = self.fetch_message_part(mail_account, num, '(BODY.PEEK[TEXT])')
			pending_messages.append({'header':header, 'body':body})

		print "Mailbox %s:%s has %s emails awaiting followup!" % (mail_account.name, followup_folder, str(len(pending_messages)))

	def fetch_message_part(self, mail_account, num, search_string):
		status, data = mail_account.imap.fetch(num, search_string)
		if status == "OK":
			return data[0][1]
		else:
			print "ERROR retrieving data for:\n %s: %s) %s" % (mail_account.name, num, search_string)
			return "ERROR"
