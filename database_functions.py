# TODO: Add unit tests
# TODO: Add error handling for database access: init, open, close, etc.

from peewee import *
from sortedcontainers import SortedDict

db = SqliteDatabase(None)


class Snippet(Model):
	name = CharField()
	category = CharField()
	language = CharField()
	keywords = CharField()
	notes = CharField()
	plain_text = CharField()
	syntax_text = CharField()

	class Meta:
		database = db


def add_data(data_dict):
	"""Create a new entry in the database.

	:param dict data_dict:  A dict containing all of the fields for a snippet
	"""

	db.connect()
	snippet = Snippet(name=data_dict['name'],
	                  category=data_dict['category'],
	                  language=data_dict['language'],
	                  keywords=data_dict['keywords'],
	                  notes=data_dict['notes'],
	                  plain_text=data_dict['plain_text'],
	                  syntax_text=data_dict['syntax_text'])
	snippet.save()
	db.close()


def create_table():
	"""Add the snippet table to the database."""

	db.connect()
	try:
		Snippet.create_table()
	except OperationalError:
		print 'Snippets table already exists!'

	db.close()


def delete_snippet(snippet_name, data_dict):
	"""Delete a snippet.

	:param str snippet_name:    The name of the snippet to delete
	:param dict data_dict:  A dict containing all of the fields for a snippet
	"""

	db.connect()

	snippet = Snippet.get(Snippet.name == snippet_name)
	snippet.delete_instance()

	db.close()


def read_db(database_file):
	"""Read the contents of the specified database.

	:param str database_file:  The full path to the database
	:return:                   A SortedDict
	:rtype: SortedDict
	"""
	snippet_dict = SortedDict()
	temp_dict1 = {}
	temp_dict2 = SortedDict()

	db.init(database_file)
	db.connect()

	for snippet in Snippet.select().order_by('category'):
		temp_dict1 = {}
		temp_dict2 = SortedDict()
		if snippet.category not in snippet_dict:
			temp_dict1['name'] = snippet.name
			temp_dict1['category'] = snippet.category
			temp_dict1['language'] = snippet.language
			temp_dict1['keywords'] = snippet.keywords
			temp_dict1['notes'] = snippet.notes
			temp_dict1['plain_text'] = snippet.plain_text
			temp_dict1['syntax_text'] = snippet.syntax_text
			temp_dict2[snippet.name] = temp_dict1
			snippet_dict[snippet.category] = temp_dict2
		else:
			temp_dict1['name'] = snippet.name
			temp_dict1['category'] = snippet.category
			temp_dict1['language'] = snippet.language
			temp_dict1['keywords'] = snippet.keywords
			temp_dict1['notes'] = snippet.notes
			temp_dict1['plain_text'] = snippet.plain_text
			temp_dict1['syntax_text'] = snippet.syntax_text
			temp_dict2[snippet.name] = temp_dict1
			snippet_dict[snippet.category].update(temp_dict2)

	db.close()

	return snippet_dict


def update_snippet(snippet_name, data_dict):
	"""Update an already existing snippet.

	:param str snippet_name:    The name of the snippet to update
	:param dict data_dict:  A dict containing all of the fields for a snippet
	"""

	db.connect()
	snippet = Snippet.get(Snippet.name==snippet_name)

	snippet.name = data_dict['name']
	snippet.category = data_dict['category']
	snippet.language = data_dict['language']
	snippet.keywords = data_dict['keywords']
	snippet.notes = data_dict['notes']
	snippet.plain_text = data_dict['plain_text']
	snippet.syntax_text = data_dict['syntax_text']

	snippet.save()

	db.close()


if __name__ == '__main__':
	# create_table()
	# data_dict = {'name': 'Create Database',
	#              'category': 'Database Functions',
	#              'language': 'Python',
	#              'keywords': 'test',
	#              'notes': 'Foo',
	#              'plain_text': """
 # def create_db():
	# db.connect()
	# try:
	# 	Snippet.create_table()
	# except OperationalError:
	# 	print 'Snippets table already exists!'""",
	#              'syntax_text': 'Foo'
	#              }
	# update_snippet('Create Database', data_dict)
	foo = read_db('snippets.sqlite')
