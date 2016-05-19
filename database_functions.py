# TODO: Create function to read database
# TODO: Add unit tests

from peewee import *
from sortedcontainers import SortedDict

db = SqliteDatabase(None)


class Snippet(Model):
	name = CharField()
	category = CharField()
	language = CharField()
	tags = CharField()
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
	                  tags=data_dict['tags'],
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

	db.init(database_file)
	db.connect()

	for snippet in Snippet.select().order_by('category'):
		if snippet.category not in snippet_dict:
			snippet_list = [snippet.category, snippet.language, snippet.tags,
			                snippet.notes, snippet.plain_text, snippet.syntax_text]
			temp_dict = SortedDict()
			temp_dict[snippet.name] = snippet_list
			snippet_dict[snippet.category] = temp_dict
		else:
			snippet_list = [snippet.category, snippet.language, snippet.tags,
			                snippet.notes, snippet.plain_text, snippet.syntax_text]
			temp_dict = SortedDict()
			temp_dict[snippet.name] = snippet_list
			snippet_dict[snippet.category].update(temp_dict)

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
	snippet.tags = data_dict['tags']
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
	#              'tags': 'test',
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
