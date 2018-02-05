#!/usr/bin/python
# -*- coding: utf-8 -*-

conf = __import__("000_conf")
lconf = __import__("700_conf")
lcommon = __import__("710_common")

import codecs
import MySQLdb
import os

from gensim import corpora, models
import gc

dictionary = corpora.Dictionary.load_from_text(lconf.suppl_730_dir+"/"+lconf.dictionary_file)


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
sql = u"SELECT rawdata_path FROM rawdata_control WHERE source = 'wos' AND entry_time < '"+lconf.datetime_trained+u"' ORDER BY entry_time DESC limit "+str(52*lconf.period_trained)+u";"
cursor.execute(sql)
rawdata_pathes = cursor.fetchall()
connector.commit()
cursor.close()

i = 0
last_rawdata = ""
for rdp in rawdata_pathes:
	files = os.listdir(rdp[0])
	if i >= lconf.limit_record4journal:
		break

	words2 = {}
	check_ut = []
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
				words_tmp = lcommon.morpheme_list(lconf.ngram, text.decode('utf-8'))
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
		last_rawdata = rdp[0] + "/" + file
#		print rdp[0], file, i, len(words2)

	####################
	# extract feature
	####################
	for so in words2.keys():
		corpus = [dictionary.doc2bow(words2[so])]
		lda = models.ldamodel.LdaModel(corpus=corpus, num_topics=lconf.lda_num_topics, id2word=dictionary, alpha=lconf.lda_alpha)

		fa = open(lconf.suppl_730_dir+"/"+so+".txt", 'a')
		for i in range(lconf.lda_num_topics):
			fa.write('TOPIC:'+str(i)+'__'+lda.print_topic(i, topn=lconf.topn).encode("utf-8")+"\r\n")
		fa.close()

	print lconf.limit_record4journal, i, len(words2), last_rawdata
	del check_ut
	del words2
	gc.collect()







