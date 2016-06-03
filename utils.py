# TODO: Add unit tests

import os

from configobj import ConfigObj
from pygments import highlight
from pygments.lexers import get_lexer_by_name
from pygments.formatters.html import HtmlFormatter
from pygments.util import ClassNotFound


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


def highlight_snippet(text, syntax):
	"""Get the correct lexer (based upon the provided syntax and highlight the text

	":param str text:       The text to highlight
	:return:                An HTML formatted string
	:rtype: str
	"""

	try:
		lexer = get_lexer_by_name(syntax)
		return highlight(text, lexer, HtmlFormatter(full=True))
	except ClassNotFound as e:
		print e
		return text


def update_languages():
	"""Read the languages file and update the Snippet Dialog combobox."""

	with open('languages.txt', 'r') as f:
		languages = f.readlines()

	with open('ui\snippet_dlg.glade', 'r') as f:
		dlg = f.readlines()

	data_start = dlg.index('    <data>\n')
	data_end = dlg.index('    </data>\n')
	del dlg[data_start + 1:data_end]

	index = data_start + 1

	for language in languages:
		if language != '':
			dlg.insert(index, '      <row>\n')
			dlg.insert(index + 1, '        <col id="0">' + language.strip() + '</col>\n')
			dlg.insert(index + 2, '      </row>\n')
			index += 3

	with open('ui\snippet_dlg.glade', 'w') as f:
		f.writelines(dlg)

