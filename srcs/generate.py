import numpy as np
import pymysql
from random import randint
import config
import srcs.database as database

def getRandomSentence():
	sid, word = getRandomWord('START')

	sentence = word
	ids = [sid]
	while word != 'END':
		sid, word = getRandomWord(word, ids)
		if word != 'END':
			sentence += ' ' + word
			ids.append(sid)

	return sentence

def getRandomWord(word, ids = []):
	db = database.DB()
	query = 'SELECT `id`, `word2`, `nb` FROM `{}` WHERE `WORD1` = %s'.format(config.twitch_channel)
	if len(ids) > 0:
		query += ' AND `id` NOT IN ({})'.format(','.join(ids))
	query += 'ORDER BY RAND() LIMIT 1000'
	
	res = np.array(db.exec(query, (word)))

	if len(res) == 0:
		return None, 'END'
	
	nbs = res[:, 2].astype(np.int)
	highest = nbs.sum()
	threshold = randint(0, highest)

	current = 0
	for i in range(len(nbs)):
		current += nbs[i]
		if current >= threshold:
			return res[i][:2]
	
	return None, 'END'
