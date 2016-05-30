from distutils.core import setup

setup(
	name='PySnippets',
	version='0.001',
	packages=[''],
	url='https://github.com/robinsiebler/PySnippet',
	license='',
	author='Robin Siebler',
	author_email='robinsiebler@dslextreme.com',
	description='A Snippet Manager created using Python and Gtk 3',
	install_requires=[
		'configobj>=5.0.6',
		'Logbook>=0.12.5',
		'peewee>=2.8.1',
		'Pygments>=2.1.3',
		'sortedcontainers>=1.4.4']
)
