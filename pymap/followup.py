import re

class ReplyReminder:
	def __init__(self, mail_account, followup_folder):
		self.status, data = mail_account.imap.select(followup_folder)

	def process_mailbox(self, mail_account, followup_folder):
		'''Retrieves and parses all mail in followup folder in preparation for notification email construction.

		All mail retrieved from the named followup_folder, and parsed into header, body, and addressing information.
		In threaded email conversations, only the latest email is retained all previous ones are ignored.
		
		Args:
			mail_account: IMAPAccount object of the currently active IMAPAccount
			followup_folder: Named folder to search for email to be processed


		Returns:
			pending_messages: A list of all parsed outstanding messages (in dict format) for notification.
		''' 
		mail_account.imap.select(followup_folder)
		status, data = mail_account.imap.search(None, "ALL")
		if status != "OK":
			print "Error Processing %s:%s" % (mail_account.name, followup_folder)
			return

		pending_messages = []
		references = []
		message_ids = data[0].split();
		if len(message_ids) > 0:
			for num in message_ids:
				header = self.fetch_message_part(mail_account, num, '(BODY.PEEK[HEADER.FIELDS (SUBJECT FROM)])')

				message_references = self.fetch_message_part(mail_account, num, '(BODY.PEEK[HEADER.FIELDS (REFERENCES)])')
				message_id = self.fetch_message_part(mail_account, num, '(BODY.PEEK[HEADER.FIELDS (MESSAGE-ID)])')
				message_id = message_id.split(": ")[1].strip()[1:-1]

				message_references = re.compile('<(.*?)>').split("".join(message_references.split()))
				message_references = filter(None, message_references[1:])
				references.extend(message_references)

				body = self.fetch_message_part(mail_account, num, '(BODY.PEEK[TEXT])')
				if message_id not in references:
					pending_messages.append({'message_id':message_id, 'header':header, 'body':body})

		return pending_messages


	def fetch_message_part(self, mail_account, num, search_string):
		''' Fetches message parts for parsing based on provided search search_string.

		Args:
			mail_account: IMAPAccount object of the currently active IMAPAccount
			num: Location of the message in the mailbox
			search_string: Search command to retrieve desired message part
		Returns:
			String containing the requested message data
		'''
		status, data = mail_account.imap.fetch(num, search_string)
		if status == "OK":
			return data[0][1]
		else:
			print "ERROR retrieving data for:\n %s: %s) %s" % (mail_account.name, num, search_string)
			return "ERROR"
