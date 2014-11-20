from ConfigParser import ConfigParser
import sys

class ConfigurationParser:
	def __init__(self):
		self.parser = ConfigParser()

	def parse_file(self,configuration_file):

		self.parser.read(configuration_file)
		if len(self.parser.sections()) < 1:
			print "ERROR: Configuration file (%s) could not be processed. \nPlease check it exists" % configuration_file
			sys.exit(1)
		else:
			for section_name in self.parser.sections():
				print 'Section: %s' % section_name
				print 'Options:'
				for name, value in self.parser.items(section_name):
					print ' %s = %s' % (name,value)

				print




