from os.path import expanduser
from ConfigParser import ConfigParser
import sys, re

class Pymap:
	def __init__(self):
		self.config = self.load_configuration_file()
		self.account_keys = self.identify_accounts(self.config)

	def load_configuration_file(self):
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
		accounts = []
		for section in config.sections():
			if "account_" in section:
				accounts.append(section)
		return account_keys


def main(argv):
	main = Pymap()


if __name__=="__main__":
	main(sys.argv[1:])