import imaplib
class IMAPAccount:
	def __init__(self, account_name, host,username,password):
		print "Checking Mail Account: %s" % account_name
		self.name = account_name
		self.imap = imaplib.IMAP4_SSL(host)
		self.status = self.connect_to_account(host, username, password)

	def connect_to_account(self, host, username, password):
		try:
			status, data = self.imap.login(username, password)
			return "OK"
		except imaplib.IMAP4.error:
			print "ERROR unable to log into %s: %s" % (self.name,host)
			return "ERROR"

	def close(self):
		self.imap.close()
		self.imap.logout()



