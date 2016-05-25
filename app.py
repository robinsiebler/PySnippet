# TODO: Get CSS Styling to work!
# TODO: Fix window resize issue!
# TODO: Create the following dialogs: Advanced Search, Create/Edit Snippet, Create/Delete Category
# TODO: Write code for menu items/toolbar buttons
# TODO: Write code to load/read settings
# TODO: Write code to load database into controls
# TODO: Add logging
# TODO: Add textview and webview to scrolled windows


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
		self.snippet_text = builder.get_object('snippet_textview')
		self.snippet_textbuffer = self.snippet_text.get_buffer()
		self.editor = WebKit.WebView()
		self.editor.set_editable(True)
		self.snippet_box.add(self.editor)
		# self.editor.load_html_string(self.db_file, "file:///") #example load string
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
				self.snippet_textbuffer.set_text('')
				if self.new_snip.get_label() == 'Edit Snippet':
					self.new_snip.set_label('New Snippet')
					self.new_snip.set_icon_widget(self.snip_new_icon)
			else:
				category = model[treeiter].parent[0]
				snippet = model[treeiter][0]
				snippet_text = self.db_contents[category][snippet]['plain_text']
				self.snippet_textbuffer.set_text(snippet_text)
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
