#!/usr/bin/python
# -*- coding: utf-8 -*-

conf = __import__("000_conf")
lcommon = __import__("710_common")
lconf = __import__("700_conf")

import codecs
import MySQLdb
import os



############################################################
# Get trained data
############################################################
# MySQL connector open
fp = open(conf.auth, 'r')
auth = fp.readline().rstrip().split(':')
fp.close()
connector = MySQLdb.connect(host="localhost", db="rawdata_control", user=auth[0], passwd=auth[1], charset="utf8")

# tmp data
tmp_data = {}
cursor = connector.cursor()
sql = u"SELECT rawdata_path FROM rawdata_control WHERE source = 'wos' AND entry_time < '"+lconf.trained_datetime+u"' ORDER BY entry_time ASC limit "+str(52*lconf.trained_period)+u";"
cursor.execute(sql)
rawdata_pathes = cursor.fetchall()
connector.commit()
cursor.close()

i = 0
words2 = {}
check_ut = []
for rdp in rawdata_pathes:
	files = os.listdir(rdp[0])
	if i > lconf.limit_feature:
		break

	for file in files:
		if ".tsv" not in file:
			continue

		flag = 0
		header_map = {}
		f = open(rdp[0]+"/"+file, 'r')
		for line in f.readlines():
			line = line.rstrip()
			cell = line.split('\t')

			# data section
			if flag == 2:
				# (exception: format broken)
				if not header_map.has_key('UT') or len(cell) < int(header_map['UT']):
					continue
				# (exception: duplicate)
				if cell[header_map['UT']] in check_ut:
					continue
				ut = cell[header_map['UT']]
				so = cell[header_map['SO']].lower()
				check_ut.append(ut)
				i += 1

				####################
				# morphological analysis
				####################
				text = " ".join([cell[header_map['TI']], cell[header_map['AB']], cell[header_map['ID']], cell[header_map['DE']]])
				words_tmp = lcommon.morpheme_list(text.decode('utf-8'))
				words2.setdefault(so, [])
				words2[so].extend(words_tmp)
				####################

			# header section
			if flag == 1:
				header_num = 0
				for k in line.split('\t'):
					header_map[str(k)] = header_num
					header_num += 1
					flag = 2
		
			if flag == 0 and line == "":
				flag = 1
		f.close()
print i


####################
# extract feature
####################
from gensim import corpora, models

dictionary = corpora.Dictionary.load_from_text(conf.suppl_720_dir+"/_dictionary.txt")
for so in words2.keys():
	corpus = [dictionary.doc2bow(words2[so])]
	lda = models.ldamodel.LdaModel(corpus=corpus, num_topics=lconf.lda_num_topics, id2word=dictionary, alpha=lconf.lda_alpha)

	fw = open(conf.suppl_720_dir+"/"+so+".txt", 'w')
	for i in range(lconf.lda_num_topics):
#		print('TOPIC:', i, '__', lda.print_topic(i, topn=lconf.topn))
#		if i % 2 == 0 or i == conf.lda_num_topics-1:
#			fw.write('TOPIC:'+str(i)+'__'+lda.print_topic(i, topn=lconf.topn).encode("utf-8")+"\r\n")
		fw.write('TOPIC:'+str(i)+'__'+lda.print_topic(i, topn=lconf.topn).encode("utf-8")+"\r\n")
	fw.close()





