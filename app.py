# TODO: Get CSS Styling to work!
# TODO: Create the following dialogs: Advanced Search, Create/Delete Category
# TODO: Write code for menu items/toolbar buttons
# TODO: Write code to load/read settings
# TODO: Write code to load database into controls
# TODO: Add logging


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
database = utils.get_db_file(config_file)

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
	def __init__(self, MainWindow):
		builder = Gtk.Builder()
		builder.add_from_file(r'ui\snippet_dlg.glade')
		builder.connect_signals(self)
		self.window = builder.get_object('snippet_dlg')
		self.txt_title = builder.get_object('txt_title')
		self.combo = builder.get_object('syntax_combobox')
		self.txt_keywords = builder.get_object('txt_keywords')
		self.notes_textview = builder.get_object('notes_txtview')
		self.snippet_textview = builder.get_object('snippet_txtview')
		self.btn_save = builder.get_object('btn_save')
		self.btn_cancel = builder.get_object('btn_cancel')

		renderer_text = Gtk.CellRendererText()
		self.combo.pack_start(renderer_text, True)
		self.combo.add_attribute(renderer_text, 'text', 0)

		self.mw = MainWindow
		self.window.set_transient_for(self.mw)
		self.window.show()

	def get_text(self, widget):
		textbuffer = widget.get_buffer()
		startiter, enditer = textbuffer.get_bounds()
		text = textbuffer.get_text(startiter, enditer, False)
		return text

	def get_combo_value(self):
		syntax = None
		tree_iter = self.combo.get_active_iter()
		if tree_iter != None:
			model = self.combo.get_model()
			syntax = model[tree_iter][0]

		print syntax

	def on_btn_click(self, button):
		btn_name = Gtk.Buildable.get_name(button)
		if btn_name == 'btn_save':
			self.title = self.txt_title.get_text()
			self.syntax = self.get_combo_value()
			self.keywords = self.txt_keywords.get_text()
			self.notes = self.get_text(self.notes_textview)
			self.snippet = self.get_text(self.snippet_textview)
			self.mw.title = self.title

			print self.title
			print self.syntax
			print  self.keywords
			print self.notes
			print self.snippet

		self.window.destroy()


class MyWindow(Gtk.ApplicationWindow):
	def __init__(self, app):
		Gtk.Window.__init__(self, title="PySnippet Manager", application=app)
		self.set_default_size(1024, 768)
		self.db_file = utils.get_db_file(config_file)
		self.db_contents = db_func.read_db(self.db_file)

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

		# screen = Gdk.Screen.get_default()
		# css_provider = Gtk.CssProvider()
		# css_provider.load_from_path('style.css')
		# context = Gtk.StyleContext()
		# context.add_provider_for_screen(screen, css_provider,
		#                                 Gtk.STYLE_PROVIDER_PRIORITY_USER)

		builder = Gtk.Builder()
		builder.add_from_file(r'ui\gui.glade')
		builder.connect_signals(self)
		self.add(builder.get_object('grid1'))
		self.new_cat = builder.get_object('New Category')
		self.del_cat = builder.get_object('Delete Category')
		self.new_snip = builder.get_object('New Snippet')
		self.del_snip = builder.get_object('Delete Snippet')
		self.adv_search = builder.get_object('Advanced Search')
		self.search = builder.get_object('Search')
		self.snip_new_icon = builder.get_object('snippet_new')
		self.snip_edit_icon = builder.get_object('snippet_edit')
		self.tree = builder.get_object('category_treeview')
		self.tree_store = builder.get_object('treestore1')
		self.snippet_box = builder.get_object('snippet_box')
		self.notes_textview = builder.get_object('notes_textview')
		self.notes_textbuffer = self.notes_textview.get_buffer()
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
		print("\"Delete Database\" activated")

	# callback function for new_cat_action
	def new_cat_callback(self, action, parameter=None):
		print("\"New Category\" activated")

	# callback function for del_cat_action
	def del_cat_callback(self, action, parameter=None):
		print("\"Delete Category\" activated")

	# callback function for new_snip_action
	def new_snip_callback(self, action, parameter=None):
		print("\"New Snippet\" activated")
		snippet_window = SnippetDialog(self)

	# callback function for del_snip_action
	def del_snip_callback(self, action, parameter=None):
		print("\"Delete Snippet\" activated")

	# callback function for advanced_search_action
	def adv_search_callback(self, action, parameter=None):
		print("\"Advanced Search\" activated")

	# callback function for search_action
	def search_callback(self, action, parameter=None):
		print("\"Search\" activated")

	# callback function for copy_action
	def copy_callback(self, action, parameter=None):
		print("\"Copy\" activated")

	# callback function for paste_action
	def paste_callback(self, action, parameter=None):
		print("\"Paste\" activated")

	# callback function for about (see the AboutDialog example)
	def about_callback(self, action, parameter=None):
		# a  Gtk.AboutDialog
		aboutdialog = Gtk.AboutDialog()

		# lists of authors and documenters (will be used later)
		authors = ["Robin Siebler"]
		documenters = ["None"]

		# we fill in the aboutdialog
		aboutdialog.set_program_name("PySnippet Manager")
		aboutdialog.set_copyright(
			"Copyright \xc2\xa9 2016 Robin Siebler")
		aboutdialog.set_authors(authors)
		aboutdialog.set_documenters(documenters)
		aboutdialog.set_website("http://www.robinsiebler.com")
		aboutdialog.set_website_label("My Website")

		# to close the aboutdialog when "close" is clicked we connect the
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

		for category in self.db_contents:
			it = self.tree_store.append(None, [category])
			for item in self.db_contents[category]:
				self.tree_store.append(it, [item])

	# ---------- Event Handlers ----------
	def on_tree_selection_changed(self, selection):
		model, treeiter = selection.get_selected()
		if treeiter is not None:
			if model[treeiter][0] in self.db_contents:  # it is a category
				self.notes_textbuffer.set_text('')
				self.editor.load_html_string(empty_snippet, "file:///")
				if self.new_snip.get_label() == 'Edit Snippet':
					self.new_snip.set_label('New Snippet')
					self.new_snip.set_icon_widget(self.snip_new_icon)
			else:
				category = model[treeiter].parent[0]
				snippet = model[treeiter][0]
				snippet_text = self.db_contents[category][snippet]['syntax_text']
				notes = self.db_contents[category][snippet]['notes']
				self.notes_textbuffer.set_text(notes)
				self.editor.load_html_string(snippet_text, "file:///")
				self.new_snip.set_label('Edit Snippet')
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

	# callback function for new
	def new_callback(self, action, parameter):
		print("You clicked \"New\"")

	# callback function for quit
	def quit_callback(self, action, parameter):
		print("You clicked \"Quit\"")
		sys.exit()
