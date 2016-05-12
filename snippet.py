# ------------------------------------------
# Name:     snippet.py
# Purpose:  snippet class
#
# Author:   Robin Siebler
# Created:  5/6/16
# ------------------------------------------


class Snippet:

	def __init__(self, name, snippet, language, tags, note):

		"""Create a snippet.

		:param str name:        The name of the snippet
		:param str snippet:     The actual snippet
		:param str language:    The language to use for syntax highlighting
		:param list tags:       A list of tags (keywords)
		:param str note:        A note associated with the snippet
		"""

		self.name = name
		self.snippet = snippet
		self.language = language
		self.tags = tags
		self.note = note


