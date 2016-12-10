# TODO: Create the following dialogs: Advanced Search, Create/Delete Category
# TODO: Write code for menu items/toolbar buttons - don't forget the menu items!
# TODO: Write code to load/read settings
# TODO: Add logging

# TODO: BUG: Key Error when changing Snippet Name during editing!

import database_functions as db_func
import gi
import os
import utils
import sys

gi.require_version('Gdk', '3.0')
gi.require_version('Gtk', '3.0')
gi.require_version('WebKit', '3.0')

from gi.repository import Gio, Gtk, WebKit

config_file = os.path.join(os.getcwd(), 'psm.ini')

empty_snippet = """
<!DOCTYPE html PUBLIC "-//W3C//DTD HTML 4.01//EN"
   "http://www.w3.org/TR/html4/strict.dtd">
<html>
	<head>
		<meta http-equiv="content-type" content="text/html; charset=None">
	        <style type="text/css">
				td.linenos { background-color: #f0f0f0; padding-right: 10px; }
				span.lineno { background-color: #f0f0f0; padding: 0 5px 0 5px; }
				pre { line-height: 125%; }
				body .hll { background-color: #ffffcc }
				body  { background: #f8f8f8; }
		    </style>
	</head>
</html>
"""


class SnippetDialog():
	"""Class to display the Create/Edit Snippet dialog and gather the data from it."""

	def __init__(self, MainWindow):
		builder = Gtk.Builder()
		builder.add_from_file(r'ui\snippet_dlg.glade')
		builder.connect_signals(self)
		self.window = builder.get_object('snippet_dlg')
		self.txt_title = builder.get_object('txt_title')
		self.combo = builder.get_object('syntax_combobox')
		self.txt_keywords = builder.get_object('txt_keywords')
		self.keywords_buffer = builder.get_object('keywords_buffer')
		self.notes_textview = builder.get_object('notes_txtview')
		self.snippet_textview = builder.get_object('snippet_txtview')
		self.btn_save = builder.get_object('btn_save')
		self.btn_cancel = builder.get_object('btn_cancel')

		renderer_text = Gtk.CellRendererText()
		self.combo.pack_start(renderer_text, True)
		self.combo.add_attribute(renderer_text, 'text', 0)

		self.mw = MainWindow
		self.window.set_transient_for(self.mw)
		if self.mw.new_snip.get_label() == 'Edit Snippet':
			self.window.set_title('Edit Snippet')
			self.txt_title.set_text(self.mw.db_contents[self.mw.current_category][self.mw.current_snippet]['name'])
			self.combo.set_active_id(self.mw.db_contents[self.mw.current_category][self.mw.current_snippet]['language'])
			self.keywords_buffer.set_text(self.mw.db_contents[self.mw.current_category][self.mw.current_snippet]['keywords'], -1)
			notes_buffer = self.notes_textview.get_buffer()
			notes_buffer.set_text(self.mw.db_contents[self.mw.current_category][self.mw.current_snippet]['notes'])
			snippet_buffer = self.snippet_textview.get_buffer()
			snippet_buffer.set_text(self.mw.db_contents[self.mw.current_category][self.mw.current_snippet]['plain_text'])

		self.window.show()

	def get_text(self, widget):
		"""Get the text from the provided widget."""

		textbuffer = widget.get_buffer()
		startiter, enditer = textbuffer.get_bounds()
		text = textbuffer.get_text(startiter, enditer, False)
		return text

	def get_combo_value(self):
		"""Get the selected entry in the combobox."""

		syntax = None
		tree_iter = self.combo.get_active_iter()
		if tree_iter is not None:
			model = self.combo.get_model()
			syntax = model[tree_iter][0]

		return syntax

	def on_btn_click(self, button):
		"""Gather the data from the dialog."""

		btn_name = Gtk.Buildable.get_name(button)
		if btn_name == 'btn_save' and self.window.get_title() == 'Create Snippet':
			self.name = self.txt_title.get_text()
			self.syntax = self.get_combo_value()
			self.keywords = self.txt_keywords.get_text()
			self.notes = self.get_text(self.notes_textview)
			self.snippet = self.get_text(self.snippet_textview)

			new_snippet = {'name': self.name,
			               'category': self.mw.current_category,
			               'language': self.syntax,
			               'keywords': self.keywords,
			               'notes': self.notes,
			               'plain_text': self.snippet,
			               'syntax_text': utils.highlight_snippet(self.snippet, self.syntax)
			               }

			db_func.add_data(new_snippet)
		elif btn_name == 'btn_save' and self.window.get_title() == 'Edit Snippet':
			self.name = self.txt_title.get_text()
			self.syntax = self.get_combo_value()
			self.keywords = self.txt_keywords.get_text()
			self.notes = self.get_text(self.notes_textview)
			self.snippet = self.get_text(self.snippet_textview)

			snippet = {'name': self.name,
			           'category': self.mw.current_category,
			           'language': self.syntax,
			           'keywords': self.keywords,
			           'notes': self.notes,
			           'plain_text': self.snippet,
			           'syntax_text': utils.highlight_snippet(self.snippet, self.syntax)
			           }
			db_func.update_snippet(self.mw.db_contents[self.mw.current_category][self.mw.current_snippet]['name'],
			                       snippet)
		elif btn_name == 'btn_cancel':
			self.window.destroy()
			return

		self.mw.db_contents = db_func.read_db(self.mw.db_file)
		self.mw.tree_store.clear()
		self.mw.populate_treeview()
		for path in self.mw.expanded_rows:
			self.mw.tree.expand_to_path(path)

		# select the previously selected entry
		self.mw.tree.row_activated(self.mw.current_selection, Gtk.TreeViewColumn(None))
		self.mw.tree.set_cursor(self.mw.current_selection)
		self.window.destroy()


class MyWindow(Gtk.ApplicationWindow):
	"""Main application window."""

	def __init__(self, app):
		Gtk.Window.__init__(self, title="PySnippet Manager", application=app)
		self.set_default_size(1024, 768)
		self.db_file = utils.get_db_file(config_file)
		self.db_contents = db_func.read_db(self.db_file)
		utils.update_languages()
		self.current_category = None
		self.current_selection = None
		self.current_snippet = None
		self.expanded_rows = []

		# action without a state created (name, parameter type)
		new_db_action = Gio.SimpleAction.new("new_db", None)
		# connected with the callback function
		new_db_action.connect("activate", self.new_db_callback)
		# added to the window
		self.add_action(new_db_action)

		# action without a state created (name, parameter type)
		new_cat_action = Gio.SimpleAction.new("new_cat", None)
		# connected with the callback function
		new_cat_action.connect("activate", self.new_cat_callback)
		# added to the window
		self.add_action(new_cat_action)

		# action without a state created (name, parameter type)
		new_snip_action = Gio.SimpleAction.new("new_snip", None)
		# connected with the callback function
		new_snip_action.connect("activate", self.new_snip_callback)
		# added to the window
		self.add_action(new_snip_action)

		# action without a state created (name, parameter type)
		copy_action = Gio.SimpleAction.new("copy", None)
		# connected with the callback function
		copy_action.connect("activate", self.copy_callback)
		# added to the window
		self.add_action(copy_action)

		# action without a state created (name, parameter type)
		paste_action = Gio.SimpleAction.new("paste", None)
		# connected with the callback function
		paste_action.connect("activate", self.paste_callback)
		# added to the window
		self.add_action(paste_action)

		# action with a state created
		about_action = Gio.SimpleAction.new("about", None)
		# action connected to the callback function
		about_action.connect("activate", self.about_callback)
		# action added to the application
		self.add_action(about_action)

		builder = Gtk.Builder()
		builder.add_from_file(r'ui\gui.glade')
		builder.connect_signals(self)
		self.add(builder.get_object('grid1'))
		self.new_cat = builder.get_object('New Category')
		self.del_cat = builder.get_object('Delete Category')
		self.del_cat.set_sensitive(False)
		self.new_snip = builder.get_object('New Snippet')
		self.new_snip.set_sensitive(False)
		self.del_snip = builder.get_object('Delete Snippet')
		self.del_snip.set_sensitive(False)
		self.adv_search = builder.get_object('Advanced Search')
		self.search = builder.get_object('Search')
		self.snip_new_icon = builder.get_object('snippet_new')
		self.snip_edit_icon = builder.get_object('snippet_edit')
		self.tree = builder.get_object('category_treeview')
		self.tree_store = builder.get_object('treestore1')
		self.snippet_box = builder.get_object('snippet_box')
		self.notes_textview = builder.get_object('notes_textview')
		self.notes_textbuffer = self.notes_textview.get_buffer()
		self.keywords_lbl = builder.get_object('keywords_lbl')
		scroll = Gtk.ScrolledWindow()
		self.editor = WebKit.WebView()
		self.editor.set_editable(True)
		self.editor.load_html_string(empty_snippet, "file:///")
		scroll.add(self.editor)
		self.snippet_box.pack_end(scroll, True, True, 0)
		self.set_position(Gtk.WindowPosition.CENTER)

		main_column = Gtk.TreeViewColumn()
		main_column.set_title("Snippets")
		cell = Gtk.CellRendererText()
		main_column.pack_start(cell, True)
		main_column.add_attribute(cell, "text", 0)
		self.populate_treeview()
		self.tree.append_column(main_column)
		self.select = self.tree.get_selection()
		self.select.connect('changed', self.on_tree_selection_changed)

	# ---------- Callback Functions ----------
	# callback function for new_db_action
	def new_db_callback(self, action, parameter=None):
		"""Display the New Database dialog and gather the desired location for the file."""

		dialog = Gtk.FileChooserDialog("Please choose a name and location for the database file", self,
		                               Gtk.FileChooserAction.SAVE,
		                               ("Select", Gtk.ResponseType.OK,
		                                Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL))
		dialog.set_default_response(Gtk.ResponseType.OK)
		dialog.set_current_name('snippets.sqlite')
		filter = Gtk.FileFilter()
		filter.set_name("Database Files")
		filter.add_pattern("*.sqlite")
		filter.add_mime_type('application/x-sqlite3')
		dialog.add_filter(filter)
		dialog.set_transient_for(self)
		dialog.set_modal(True)
		response = dialog.run()
		if response == Gtk.ResponseType.OK:
			self.db_file = dialog.get_filename()

		dialog.destroy()

	# callback function for del_db_action
	def del_db_callback(self, action, parameter=None):
		"""Delete the specified database."""

		print("\"Delete Database\" activated")

	# callback function for new_cat_action
	def new_cat_callback(self, action, parameter=None):
		"""Create a new category."""

		print("\"New Category\" activated")

	# callback function for del_cat_action
	def del_cat_callback(self, action, parameter=None):
		"""Delete the specified category."""

		print("\"Delete Category\" activated")

	# callback function for new_snip_action
	def new_snip_callback(self, action, parameter=None):
		"""Create/Edit a snippet"""

		# save the currently selected entry so it can be selected again after the treeview reloads
		if self.new_snip.get_label() == 'Edit Snippet':
			self.current_selection = self.tree.get_cursor()[0]
		snippet_window = SnippetDialog(self)

	# callback function for del_snip_action
	def del_snip_callback(self, action, parameter=None):
		"""Delete a snippet."""

		print("\"Delete Snippet\" activated")

	# callback function for advanced_search_action
	def adv_search_callback(self, action, parameter=None):
		"""Display the Advanced Search Dialog."""

		print("\"Advanced Search\" activated")

	# callback function for search_action
	def search_callback(self, action, parameter=None):
		"""Perform a basic search."""

		print("\"Search\" activated")

	# callback function for copy_action
	def copy_callback(self, action, parameter=None):
		"""Copy the selected snippet and/or selected text ???"""

		print("\"Copy\" activated")

	# callback function for paste_action
	def paste_callback(self, action, parameter=None):
		"""Paste the selected snippet and/or selected text ???"""
		print("\"Paste\" activated")

	# callback function for about (see the AboutDialog example)
	def about_callback(self, action, parameter=None):
		"""Display the About Dialog."""

		aboutdialog = Gtk.AboutDialog()

		# lists of authors
		authors = ["Robin Siebler"]

		# fill in the aboutdialog
		aboutdialog.set_program_name("PySnippet Manager")
		aboutdialog.set_copyright(
			"Copyright \xc2\xa9 2016 Robin Siebler")
		aboutdialog.set_authors(authors)
		aboutdialog.set_website("http://www.robinsiebler.com")
		aboutdialog.set_website_label("My Website")

		# to close the aboutdialog when "close" is clicked, connect the
		# "response" signal to on_close
		aboutdialog.connect("response", self.on_close)
		# show the aboutdialog
		aboutdialog.set_transient_for(self)
		aboutdialog.set_position(Gtk.WindowPosition.CENTER)
		aboutdialog.show()

	# a callback function to destroy the aboutdialog
	def on_close(self, action, parameter):
		action.destroy()

	def populate_treeview(self):
		"""Populate the treeview with the DB Snippet Categories and Snippet Titles."""

		for category in self.db_contents:
			it = self.tree_store.append(None, [category])
			for item in self.db_contents[category]:
				self.tree_store.append(it, [item])

	# ---------- Event Handlers ----------
	def on_row_collapsed(self, tree_view, tree_iter, path):
		"""Remove row from the list of rows to expand when the treeview is re-created."""

		if path in self.expanded_rows:
			self.expanded_rows.remove(path)

	def on_row_expanded(self, tree_view, tree_iter, path):
		"""Add row to the list of rows to expand when the treeview is re-created."""

		if path not in self.expanded_rows:
			self.expanded_rows.append(path)

	def on_tree_selection_changed(self, selection):
		"""Perform various actions when a Snippet or Category is selected."""

		model, treeiter = selection.get_selected()
		if treeiter is not None:
			if model[treeiter][0] in self.db_contents:  # it is a category
				self.del_cat.set_sensitive(True)
				self.new_snip.set_sensitive(True)
				self.del_snip.set_sensitive(False)
				self.current_category = model[treeiter][0]
				self.notes_textbuffer.set_text('')
				self.keywords_lbl.set_text('Keywords:')
				self.editor.load_html_string(empty_snippet, "file:///")
				if self.new_snip.get_label() == 'Edit Snippet':
					self.new_snip.set_label('New Snippet')
					self.new_snip.set_tooltip_text('Add a New Snippet')
					self.new_snip.set_icon_widget(self.snip_new_icon)
			else:
				self.current_category = model[treeiter].parent[0]
				self.current_snippet = model[treeiter][0]
				self.del_cat.set_sensitive(False)
				self.del_snip.set_sensitive(True)
				snippet_text = self.db_contents[self.current_category][self.current_snippet]['syntax_text']
				notes = self.db_contents[self.current_category][self.current_snippet]['notes']
				self.notes_textbuffer.set_text(notes)
				self.keywords_lbl.set_text('Keywords: ' + self.db_contents[self.current_category][self.current_snippet]['keywords'])
				self.editor.load_html_string(snippet_text, "file:///")
				self.new_snip.set_label('Edit Snippet')
				self.new_snip.set_tooltip_text('Edit Selected Snippet')
				self.new_snip.set_icon_widget(self.snip_edit_icon)


class MyApplication(Gtk.Application):

	def __init__(self):
		Gtk.Application.__init__(self)

	def do_activate(self):
		win = MyWindow(self)
		win.show_all()

	def do_startup(self):
		# FIRST THING TO DO: do_startup()
		Gtk.Application.do_startup(self)

		# action without a state created
		quit_action = Gio.SimpleAction.new("quit", None)
		# action connected to the callback function
		quit_action.connect("activate", self.quit_callback)
		# action added to the application
		self.add_action(quit_action)

		# a builder to add the menu to the grid:
		builder = Gtk.Builder()
		# get the file (if it is there)
		try:
			builder.add_from_file(r'ui\menu.xml')
		except:
			print("file not found")
			sys.exit()

		# we use the method Gtk.Application.set_menubar(menubar) to add the menubar
		# and the menu to the application (Note: NOT the window!)
		self.set_menubar(builder.get_object("menubar"))
		self.set_app_menu(builder.get_object("appmenu"))

	# callback function for quit
	def quit_callback(self, action, parameter):
		sys.exit()
