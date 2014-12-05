from os.path import expanduser
from ConfigParser import ConfigParser, NoOptionError
from account import IMAPAccount
from followup import ReplyReminder
from message import MessageBuilder
import sys, re

class Pymap:
	def __init__(self):
		config = self.load_configuration_file()
		account_keys = self.identify_accounts(config)
		self.process_accounts(account_keys, config)

	def load_configuration_file(self):
		''' Loads configuration file from users home directory.'''
		user_home = expanduser("~")
		configuration_file = user_home + "/.pymaprc"
		parser = ConfigParser()
		parser.read(configuration_file)
		if len(parser.sections()) < 1:
			print "ERROR: Configuration file (%s) could not be processed. \nPlease check it exists" % configuration_file
			sys.exit(1)
		else:
			print "Loaded Configuration File"
			return parser

	def identify_accounts(self,config):
		''' Returns a list of keys for account configuration options'''
		account_keys = []
		for section in config.sections():
			if "account_" in section:
				account_keys.append(section)
		return account_keys

	def process_accounts(self, account_keys, config):
		''' Connect to, and process email in the named folder of all specified accounts.

		Steps through each account specified in the configuration file and checks for a valid connection.
		When a connection is made, checks for the presnece of the named folder, and if one exists processes it.

		Args:
			account_keys: List of all configuration keys relating to an account section.
			config: configuration object.
		'''
		for account in account_keys:
			try:
				host = config.get(account, 'host')
				username = config.get(account, 'username')
				password = config.get(account, 'password')
				email_address = config.get(account, 'email_address')
			except NoOptionError, e:
				print "ERROR Parsing Configuration Options for: %s" % account
				print e

			mail_account = IMAPAccount(account, host, username, password)

			if mail_account.status == "OK":
				try:
					followup_folder = config.get(account, 'followup_folder')
				except NoOptionError, e:
					print "ERROR Parsing Configuration Options for: %s" % account_name
					print e
				personal_name = config.get("config", "name")
				reply_remind = ReplyReminder(mail_account, followup_folder)
				if reply_remind.status == "OK":
					# Folder Found, Process Mailbox
					pending_messages = reply_remind.process_mailbox(mail_account, followup_folder)
					if len(pending_messages) > 0:
						builder = MessageBuilder()
						builder.send_followup(pending_messages, mail_account, email_address, personal_name)
						print "Mailbox %s:%s has %d emails awaiting followup!" % (mail_account.name, followup_folder, len(pending_messages))
					else:
						print "Great Job! Mailbox %s:%s has no outstanding emails!" % (mail_account.name, followup_folder)

				mail_account.close()


def main(argv):
	main = Pymap()


if __name__=="__main__":
	main(sys.argv[1:])