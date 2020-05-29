import numpy as np
import pymysql
import sys
import config

class DB:
	def connect(self):
		self.db = pymysql.connect('localhost', config.db_username, config.db_password, config.db_name)
	
	def disconnect(self):
		self.db.close()
	
	def exec(self, query, *params):
		self.connect()

		with self.db.cursor() as cursor:
			cursor.execute(query, *params)
			if 'INSERT' in query:
				self.db.commit()
			res = cursor.fetchall()

		self.disconnect()
		return res

	def insert_words(self, chains):
		values = ','.join(['(%s, %s, 1)' for i in range(int(len(chains) / 2))])
		query = 'INSERT INTO `{}` (`word1`, `word2`, `nb`) VALUES {} ON DUPLICATE KEY UPDATE `nb` = `nb` + 1;'.format(config.twitch_channel, values)
		self.exec(query, (chains))

