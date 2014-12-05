import imaplib
import time
import email.message
import random

class MessageBuilder():

	def send_followup(self, pending_messages, mail_account, email_address, personal_name=""):
		'''Create the followup notification email.

		Creates a new email Message object with the provided destination information, and inserts the followup message into the mail account's INBOX.

		Args:
			pending_messages: List of dict objects containing the pending email details.
			mail_account: IMAPAccount object for currently active IMAPAccount.
			email_address: Email address string to be inserted as the from/to email.
			personal_name: Friendly name to start off the constructed email. [default='']
		'''
		new_message = email.message.Message()
		new_message['Subject'] = 'Some Emails Need Your Attention!'
		new_message['From'] = email_address
		new_message['To'] = email_address
		new_message.set_payload(self.build_message_string(mail_account,pending_messages,personal_name))

		try:
			mail_account.imap.append('INBOX','', imaplib.Time2Internaldate(time.time()), str(new_message))
		except Exception, e:
			print e

	def build_message_string(self,mail_account,pending_messages,personal_name=''):
		'''Builds the body of the notification email.

		Builds a string containing the total number of outstanding emails.
		Lists (up to) 5 randomly selected ones to provide the subject & from information.

		Args:
			mail_account: IMAPAccount Ojbect for currently active IMAPAccount.
			pending_messages: List of dict objects containing the pending email details.
			personal_name: Friendly name to start off the constructed email. [default='']

		Returns:
			message_string: The email message body
		'''
		message_string = ""
		if personal_name is not "":
			message_string += "Hi %s,\n\n" % personal_name

		message_string += "You've currently got %d emails that are waiting on a response from you! " % len(pending_messages)

		if len(pending_messages) > 5:
			message_string += "Why not tackle a few today? Here's a random selection of 5 from your list:\n\n"

			for message in random.sample(pending_messages, 5):
				message_string += self.format_pending_message(message)
		else:
			message_string += "Why not tackle them today? \n\n"
			for message in pending_messages:
				message_string += "\n"
				message_string += self.format_pending_message(message)
				message_string += "\n"

		return message_string

	def format_pending_message(self, message):
		'''Helper method returns formatted From/Subject elements of the email.'''
		message_string = ""
		for item in message['header'].split("\n"):
			if "From:" in item:
				message_string += unicode(item.strip()) + "\n"
			if "Subject:" in item:
				message_string += "     " + unicode(item.strip().decode('utf-8'))
		return message_string