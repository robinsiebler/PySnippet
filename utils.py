# TODO: Add unit tests

import os

from configobj import ConfigObj
from pygments import highlight
from pygments.lexers.python import PythonLexer
from pygments.formatters.html import HtmlFormatter


def get_db_file(config_file):
	"""Return the full path to the database file.

	:param str config_file:     The full path to the config file
	:return:                    The full path to the database file
	:rtype: str
	"""

	db = read_db_setting(config_file)
	if db:
		if not os.path.exists(db):
			print 'ERROR: The database file ' + db + ' does not exist'
		else:
			return db
	# if the
	db = os.path.join(os.getcwd(), 'snippets.sqlite')

	return db


def read_db_setting(config_file):
	"""Read the database setting from the INI file (if they exist).

	:return:    The database path or None if it does not exist.
	:rtype: str
	"""

	database = None
	if os.path.exists(config_file):
		try:
			database = get_settings('General', config_file)['database']
		except KeyError:
			print("exception on %s!" % 'database')

	return database


def get_settings(section, config_file):
	"""Read a given section from a config file and return it.

	:param str section:         The section to read
	:param str  config_file:    The file to read from
	:return:                    A dictionary of settings
	:rtype: dict
	"""

	settings = {}
	config = ConfigObj(config_file)

	try:
		settings = config[section]
	except KeyError:
		print("exception on %s!" % section)
		settings = None
	return settings
