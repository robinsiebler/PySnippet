import os

from ConfigParser import ConfigParser
from pygments import highlight
from pygments.lexers.python import PythonLexer
from pygments.formatters.html import HtmlFormatter


def create_db_path(directory):
	"""Create a new database for snippets.

	:param str directory:   Directory to create the file in
	"""

	try:
		if not os.path.exists(directory):
			os.mkdir(directory)
	except WindowsError:
		print 'ERROR! Unable to create the folder: ' + directory
		return False

	return True


def read_database_setting():
	"""Read the database setting from the INI file (if they exist).

	:return:    The database path or None if it does not exist.
	:rtype: str
	"""

	config_file = os.path.join(os.getcwd(), 'psm.ini')
	if os.path.exists(config_file):
		database = get_settings('Database', config_file)
	else:
		return None

	return database


def get_settings(section, config_file):
	"""Read a given section from a config file and return it.

	:param str section:         The section to read
	:param str  config_file:    The file to read from
	:return:                    A dictionary of settings
	:rtype: dict
	"""

	config = ConfigParser()
	config.read(config_file)

	dict1 = {}
	options = config.options(section)
	for option in options:
		try:
			dict1[option] = config.get(section, option)
			if dict1[option] == -1:
				print("skip: %s" % option)
		except:
			print("exception on %s!" % option)
			dict1[option] = None
	return dict1
