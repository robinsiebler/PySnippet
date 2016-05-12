import sys

from app import MyApplication


if __name__ == '__main__':
	app = MyApplication()
	exit_status = app.run(sys.argv)
	sys.exit(exit_status)