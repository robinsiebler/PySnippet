import gi
import sys

gi.require_version('Gdk', '3.0')
gi.require_version('Gtk', '3.0')
gi.require_version('WebKit', '3.0')

from gi.repository import Gio, Gtk, WebKit


class MyWindow(Gtk.ApplicationWindow):
	def __init__(self, app):
		Gtk.Window.__init__(self, title="PySnippet Manager", application=app)
		self.set_default_size(800, 600)

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
		self.add(builder.get_object('grid1'))
		self.snippet_box = builder.get_object('snippet_box')
		self.editor = WebKit.WebView()
		self.editor.set_editable(True)
		self.snippet_box.add(self.editor)
		self.editor.load_html_string('This is a test', "file:///")

		self.set_position(Gtk.WindowPosition.CENTER)




	# callback function for copy_action
	def copy_callback(self, action, parameter):
		print("\"Copy\" activated")


	# callback function for paste_action
	def paste_callback(self, action, parameter):
		print("\"Paste\" activated")


	# callback function for about (see the AboutDialog example)
	def about_callback(self, action, parameter):
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
		new_action = Gio.SimpleAction.new("new", None)
		# action connected to the callback function
		new_action.connect("activate", self.new_callback)
		# action added to the application
		self.add_action(new_action)

		# action without a state created
		quit_action = Gio.SimpleAction.new("quit", None)
		# action connected to the callback function
		quit_action.connect("activate", self.quit_callback)
		# action added to the application
		self.add_action(quit_action)

		# a builder to add the UI designed with Glade to the grid:
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



