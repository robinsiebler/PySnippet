# TODO: Get CSS Styling to work!
# TODO: Fix window resize issue!
# TODO: Create the following dialogs: Advanced Search, New Database, Create/Edit Snippet, Create/Delete Category
# TODO: Write code for menu items/toolbar buttons
# TODO: Write code to load/read settings
# TODO: Add logging


import gi
import os
import utils
import sys

gi.require_version('Gdk', '3.0')
gi.require_version('Gtk', '3.0')
gi.require_version('WebKit', '3.0')

from gi.repository import Gdk, Gio, Gtk, WebKit

config_file = os.path.join(os.getcwd(), 'psm.ini')
database = utils.get_db_file(config_file)


ui="""<interface>
  <requires lib="gtk+" version="3.10"/>
  <object class="GtkListStore" id="category_liststore"/>
  <object class="GtkImage" id="folder_delete">
    <property name="visible">True</property>
    <property name="can_focus">False</property>
    <property name="pixbuf">icons\folder_delete.png</property>
  </object>
  <object class="GtkImage" id="folder_new">
    <property name="visible">True</property>
    <property name="can_focus">False</property>
    <property name="pixbuf">icons\folder_add.png</property>
  </object>
  <object class="GtkImage" id="search">
    <property name="visible">True</property>
    <property name="can_focus">False</property>
    <property name="pixbuf">icons\system-search-4.png</property>
  </object>
  <object class="GtkImage" id="snippet_delete">
    <property name="visible">True</property>
    <property name="can_focus">False</property>
    <property name="pixbuf">icons\page_white_delete.png</property>
  </object>
  <object class="GtkImage" id="snippet_new">
    <property name="visible">True</property>
    <property name="can_focus">False</property>
    <property name="pixbuf">icons\document-new-6.png</property>
  </object>
  <object class="GtkGrid" id="grid1">
    <property name="visible">True</property>
    <property name="can_focus">False</property>
    <child>
      <object class="GtkBox" id="box1">
        <property name="width_request">-1</property>
        <property name="height_request">-1</property>
        <property name="visible">True</property>
        <property name="can_focus">False</property>
        <property name="hexpand">True</property>
        <property name="vexpand">True</property>
        <property name="orientation">vertical</property>
        <child>
          <object class="GtkBox" id="box5">
            <property name="visible">True</property>
            <property name="can_focus">False</property>
            <child>
              <object class="GtkToolbar" id="toolbar1">
                <property name="visible">True</property>
                <property name="can_focus">False</property>
                <property name="hexpand">True</property>
                <property name="toolbar_style">both</property>
                <property name="icon_size">2</property>
                <child>
                  <object class="GtkToolButton" id="btn_new_category">
                    <property name="visible">True</property>
                    <property name="can_focus">False</property>
                    <property name="tooltip_text" translatable="yes">Add a New Category</property>
                    <property name="label" translatable="yes">New Category</property>
                    <property name="use_underline">True</property>
                    <property name="icon_widget">folder_new</property>
                  </object>
                  <packing>
                    <property name="expand">False</property>
                    <property name="homogeneous">True</property>
                  </packing>
                </child>
                <child>
                  <object class="GtkToolButton" id="btn_delete_category">
                    <property name="visible">True</property>
                    <property name="can_focus">False</property>
                    <property name="tooltip_text" translatable="yes">Remove the selected category</property>
                    <property name="label" translatable="yes">Delete Category</property>
                    <property name="use_underline">True</property>
                    <property name="icon_widget">folder_delete</property>
                  </object>
                  <packing>
                    <property name="expand">False</property>
                    <property name="homogeneous">True</property>
                  </packing>
                </child>
                <child>
                  <object class="GtkToolButton" id="New Snippet">
                    <property name="visible">True</property>
                    <property name="can_focus">False</property>
                    <property name="tooltip_text" translatable="yes">Add a New Snippet</property>
                    <property name="label" translatable="yes">New Snippet</property>
                    <property name="use_underline">True</property>
                    <property name="icon_widget">snippet_new</property>
                  </object>
                  <packing>
                    <property name="expand">False</property>
                    <property name="homogeneous">True</property>
                  </packing>
                </child>
                <child>
                  <object class="GtkToolButton" id="Delete Snippet">
                    <property name="visible">True</property>
                    <property name="can_focus">False</property>
                    <property name="tooltip_text" translatable="yes">Delete Snippet</property>
                    <property name="label" translatable="yes">Delete Snippet</property>
                    <property name="use_underline">True</property>
                    <property name="icon_widget">snippet_delete</property>
                  </object>
                  <packing>
                    <property name="expand">False</property>
                    <property name="homogeneous">True</property>
                  </packing>
                </child>
                <child>
                  <object class="GtkSeparatorToolItem" id="separator1">
                    <property name="visible">True</property>
                    <property name="can_focus">False</property>
                  </object>
                  <packing>
                    <property name="expand">False</property>
                    <property name="homogeneous">True</property>
                  </packing>
                </child>
                <child>
                  <object class="GtkToolButton" id="Search">
                    <property name="visible">True</property>
                    <property name="can_focus">False</property>
                    <property name="tooltip_text" translatable="yes">Advanced Search</property>
                    <property name="label" translatable="yes">Advanced Search</property>
                    <property name="use_underline">True</property>
                    <property name="icon_widget">search</property>
                  </object>
                  <packing>
                    <property name="expand">False</property>
                    <property name="homogeneous">True</property>
                  </packing>
                </child>
              </object>
              <packing>
                <property name="expand">False</property>
                <property name="fill">True</property>
                <property name="position">0</property>
              </packing>
            </child>
            <child>
              <object class="GtkSearchEntry" id="searchentry1">
                <property name="visible">True</property>
                <property name="can_focus">True</property>
                <property name="primary_icon_name">edit-find-symbolic</property>
                <property name="primary_icon_activatable">False</property>
                <property name="primary_icon_sensitive">False</property>
              </object>
              <packing>
                <property name="expand">False</property>
                <property name="fill">True</property>
                <property name="position">1</property>
              </packing>
            </child>
          </object>
          <packing>
            <property name="expand">False</property>
            <property name="fill">True</property>
            <property name="position">1</property>
          </packing>
        </child>
        <child>
          <object class="GtkBox" id="box2">
            <property name="visible">True</property>
            <property name="can_focus">False</property>
            <property name="homogeneous">True</property>
            <child>
              <object class="GtkTreeView" id="category_treeview">
                <property name="visible">True</property>
                <property name="can_focus">True</property>
                <property name="model">category_liststore</property>
                <child internal-child="selection">
                  <object class="GtkTreeSelection" id="treeview-selection"/>
                </child>
              </object>
              <packing>
                <property name="expand">True</property>
                <property name="fill">True</property>
                <property name="position">0</property>
              </packing>
            </child>
            <child>
              <object class="GtkBox" id="snippet_box">
                <property name="visible">True</property>
                <property name="can_focus">False</property>
                <property name="margin_right">2</property>
                <property name="orientation">vertical</property>
                <property name="homogeneous">True</property>
                <child>
                  <object class="GtkListBox" id="listbox1">
                    <property name="visible">True</property>
                    <property name="can_focus">False</property>
                  </object>
                  <packing>
                    <property name="expand">True</property>
                    <property name="fill">True</property>
                    <property name="position">0</property>
                  </packing>
                </child>
                <child>
                  <object class="GtkBox" id="box3">
                    <property name="visible">True</property>
                    <property name="can_focus">False</property>
                    <child>
                      <object class="GtkBox" id="box4">
                        <property name="visible">True</property>
                        <property name="can_focus">False</property>
                        <property name="orientation">vertical</property>
                        <child>
                          <object class="GtkLabel" id="label1">
                            <property name="visible">True</property>
                            <property name="can_focus">False</property>
                            <property name="label" translatable="yes">label</property>
                          </object>
                          <packing>
                            <property name="expand">False</property>
                            <property name="fill">True</property>
                            <property name="position">0</property>
                          </packing>
                        </child>
                        <child>
                          <object class="GtkLabel" id="label2">
                            <property name="visible">True</property>
                            <property name="can_focus">False</property>
                            <property name="label" translatable="yes">label</property>
                          </object>
                          <packing>
                            <property name="expand">False</property>
                            <property name="fill">True</property>
                            <property name="position">1</property>
                          </packing>
                        </child>
                      </object>
                      <packing>
                        <property name="expand">True</property>
                        <property name="fill">True</property>
                        <property name="position">0</property>
                      </packing>
                    </child>
                    <child>
                      <object class="GtkTextView" id="textview1">
                        <property name="visible">True</property>
                        <property name="can_focus">True</property>
                      </object>
                      <packing>
                        <property name="expand">True</property>
                        <property name="fill">True</property>
                        <property name="position">1</property>
                      </packing>
                    </child>
                  </object>
                  <packing>
                    <property name="expand">True</property>
                    <property name="fill">True</property>
                    <property name="position">1</property>
                  </packing>
                </child>
                <child>
                  <placeholder/>
                </child>
              </object>
              <packing>
                <property name="expand">True</property>
                <property name="fill">True</property>
                <property name="position">1</property>
              </packing>
            </child>
          </object>
          <packing>
            <property name="expand">True</property>
            <property name="fill">True</property>
            <property name="position">2</property>
          </packing>
        </child>
      </object>
      <packing>
        <property name="left_attach">0</property>
        <property name="top_attach">0</property>
      </packing>
    </child>
  </object>
</interface>
"""


class MyWindow(Gtk.ApplicationWindow):
	def __init__(self, app):
		Gtk.Window.__init__(self, title="PySnippet Manager", application=app)
		self.set_default_size(800, 600)

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

		screen = Gdk.Screen.get_default()
		css_provider = Gtk.CssProvider()
		css_provider.load_from_path('style.css')
		context = Gtk.StyleContext()
		context.add_provider_for_screen(screen, css_provider,
		                                Gtk.STYLE_PROVIDER_PRIORITY_USER)

		builder = Gtk.Builder()
		builder.add_from_string(ui)
		self.add(builder.get_object('grid1'))
		self.snippet_box = builder.get_object('snippet_box')
		self.editor = WebKit.WebView()
		self.editor.set_editable(True)
		self.snippet_box.add(self.editor)
		self.editor.load_html_string('This is a test', "file:///")
		self.set_position(Gtk.WindowPosition.CENTER)

		screen = Gdk.Screen.get_default()
		css_provider = Gtk.CssProvider()
		css_provider.load_from_path('style.css')
		context = Gtk.StyleContext()
		context.add_provider_for_screen(screen, css_provider,
		                                Gtk.STYLE_PROVIDER_PRIORITY_USER)

	# callback function for copy_action
	def new_db_callback(self, action, parameter):
		print("\"New Database\" activated")

	# callback function for copy_action
	def new_cat_callback(self, action, parameter):
		print("\"New Category\" activated")

	# callback function for copy_action
	def new_snip_callback(self, action, parameter):
		print("\"New Snippet\" activated")

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

		# # action without a state created
		# new_action = Gio.SimpleAction.new("new", None)
		# # action connected to the callback function
		# new_action.connect("activate", self.new_callback)
		# # action added to the application
		# self.add_action(new_action)

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


if __name__ == '__main__':
	app = MyApplication()
	exit_status = app.run(sys.argv)
	sys.exit(exit_status)