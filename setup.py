import sys

from srcs.database import DB
import config

def readFile(filename):
	with open(filename) as f:
		return f.read()

def userConfirmation(q):
	reply = str(input(q + ' (y/n): ')).lower().strip()
	if reply[0] == 'y':
		return True
	return False

def tableExists(db):
	exists = db.exec('SHOW TABLES LIKE %s', (config.twitch_channel))
	return len(exists) != 0

def up(db):
	if tableExists(db):
		print('Table `{}` already exists, exiting...'.format(config.twitch_channel))
		sys.exit()
	query = readFile('srcs/db.sql')
	db.exec(query.format(config.twitch_channel))

def down(db):
	if not tableExists(db):
		print('Table `{}` does not exists, exiting...'.format(config.twitch_channel))
		sys.exit()
	db.exec('DROP TABLE `{}`'.format(config.twitch_channel))

def main():
	db = DB()

	if len(sys.argv) == 2 and sys.argv[1] == '--rollback':
		if not userConfirmation('Are you sure you want to drop table `{}` ?'.format(config.twitch_channel)):
			print('aborted..')
		else:	
			down(db)
			print('Table `{}` dropped successfully'.format(config.twitch_channel))
	else:
		up(db)
		print('Table `{}` created successfully'.format(config.twitch_channel))

if __name__ == '__main__':
	main()

