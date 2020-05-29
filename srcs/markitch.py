import sys
import irc.bot
import logging
from srcs.generate import getRandomSentence
from srcs.database import DB
import config

class TwitchBot(irc.bot.SingleServerIRCBot):
	def __init__(self, logfile):
		self.token = config.twitch_oauth
		self.channel = '#' + config.twitch_channel
		self.logger = getLogger(logfile)

		server = 'irc.chat.twitch.tv'
		port = 6667
		self.logger.info('Connecting to ' + server + ' on port ' + str(port) + '...')
		irc.bot.SingleServerIRCBot.__init__(self, [(server, port, 'oauth:' + self.token)], config.twitch_username, config.twitch_username)

	def on_welcome(self, c, e):
		self.logger.info('Joining ' + self.channel)

		c.cap('REQ', ':twitch.tv/commands')
		c.cap('REQ', ':twitch.tv/tags')
		c.join(self.channel)
		self.logger.info('Statring to log messages...')
	
	def on_pubmsg(self, c, e):
		msg = e.arguments[0]
		self.logger.debug('Received msg: '+msg)

		if msg[0] == '!':
			if msg == config.twitch_command:
				self.logger.info('Markov chain requested')
				self.logger.info('Genrating chain...')
				chatMsg = getRandomSentence()
				
				self.logger.info('Sending irc chat: `'+chatMsg+'`')
				self.do_command(chatMsg)
			return
		
		for tag in e.tags:
			if tag['key'] == 'display-name' and tag['value'] in config.twitch_channel_bots:
				self.logger.info('Ignoring message...')
				return				

		words = msg.split()
		if 'START' in words or 'END' in words:
			return
		
		words.insert(0, 'START')
		words.append('END')

		processChain(words)	

	def do_command(self, msg):
		c = self.connection
		res = c.privmsg(self.channel, msg)

def processChain(words):
	res = []	
	
	if len(words[0]) > 255:
		return
	for i in range(1, len(words)):
		if len(words[i]) > 255:
			return
		res.append(words[i - 1])
		res.append(words[i])
	
	db = DB()
	sq = db.insert_words(res)

def getLogger(logf):
	logger = logging.getLogger('markitch_daemon')
	logger.setLevel(config.log_level)

	fh = logging.FileHandler(logf)
	fh.setLevel(config.log_level)

	formatstr = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
	formatter = logging.Formatter(formatstr)

	fh.setFormatter(formatter)

	logger.addHandler(fh)
	return logger

def main(logfile):
	bot = TwitchBot(logfile)
	bot.start()
