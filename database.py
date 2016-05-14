import utils

from peewee import *

database = SqliteDatabase(utils.get_database())

class Snippet(Model):
	name = CharField()
	category = CharField()
	language = CharField()
	tags = CharField()
	notes = CharField()
	plain_text = CharField()
	syntax_text = CharField()

	class Meta:
		database = database
