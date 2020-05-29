from lockfile.pidlockfile import PIDLockFile
from lockfile import AlreadyLocked

import argparse
import daemon
import os
import signal
import sys

import srcs.markitch as markitch

def start_daemon(args):
	if not os.path.exists(args.logdir) or not os.access(args.logdir, os.W_OK):
		print('ERROR: Cannot access log dir', args.logdir)
		print('Make sure the directory exists and is writeable')
		sys.exit()

	if not os.path.exists(args.piddir) or not os.access(args.piddir, os.W_OK):
		print('ERROR: Cannot access pid dir', args.piddir)
		print('Make sure the directory exists and is writeable')
		sys.exit()

	try:
		pf = PIDLockFile(args.piddir+'daemon.pid', timeout=-1)
		pf.acquire()
		print('lock acquired')
		pf.break_lock()
	except AlreadyLocked:	
		try:
			pid = pf.read_pid()
			os.kill(pid, 0)
			print('Process already running with PID:', pid, 'exiting...')
			sys.exit()
		except OSError:
			pf.break_lock()
	
	print('Daemon started')

	with open(args.logdir + 'error.log', 'w') as err:	
		with daemon.DaemonContext(
			working_directory=os.getcwd(),
			pidfile=pf,
			stderr=err,
		) as context:
			markitch.main(args.logdir + 'daemon.log')
	
def stop_daemon(args):
	try:
		pf = PIDLockFile(args.piddir+'daemon.pid', timeout=-1)
		pf.acquire()
		print('Deamon is not running, exiting...')
		pf.break_lock()
	except AlreadyLocked:
		pid = pf.read_pid()
		try:
			# checking if process is runnning...
			os.kill(pid, 0)
			os.kill(pid, signal.SIGTERM)
			pf.break_lock()
			print('Daemon killed:', pid)
		except OSError:
			print('Deamon is not running, exiting...')

if __name__ == '__main__':
	parser = argparse.ArgumentParser(description='Markitch daeomon handler')
	parser.add_argument('action', choices=['start', 'stop'])
	parser.add_argument('-l', '--logdir', help='Path to the daemon log dirrectory', default='/var/log/markitch/')
	parser.add_argument('-p', '--piddir', help='Path to the daemon pid dirrectory', default=os.path.expanduser('~') + '/.run/markitch/')

	args = parser.parse_args()
	if args.action == 'start':
		start_daemon(args)
	else:
		stop_daemon(args)	
