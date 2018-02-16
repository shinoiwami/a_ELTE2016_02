#!/usr/bin/python
# -*- coding: utf-8 -*-

conf = __import__("000_conf")
lconf = __import__("700_conf")
lcommon = __import__("710_common")

import codecs
import MySQLdb
import re
import os
import sys

from gensim import corpora, models

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
sql = u"SELECT rawdata_path FROM rawdata_control WHERE source = 'wos' AND entry_time >= '"+lconf.datetime_s_trained+u"' AND entry_time < '"+lconf.datetime_e_trained+u"' ORDER BY entry_time DESC;"

cursor.execute(sql)
rawdata_pathes = cursor.fetchall()
connector.commit()
cursor.close()

i = 0
last_rawdata = ""
check_rdp = []
for rdp in rawdata_pathes:
	if rdp[0] in check_rdp:
		continue
	check_rdp.append(rdp[0])
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
				so = re.sub(r'[/]+', '', so)
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

	####################
	# extract feature
	####################
	for so in words2.keys():
		# log
		fa = open("730_2.log", 'a')
		fa.write("["+so+"]: Start extract feature\r\n")
		fa.write("["+so+"]: 104\r\n")
		corpus = [dictionary.doc2bow(words2[so])]
		fa.write("["+so+"]: 106\r\n")
		lda = models.ldamodel.LdaModel(corpus=corpus, num_topics=lconf.lda_num_topics, id2word=dictionary, alpha=lconf.lda_alpha)

		fa.write("["+so+"]: 109\r\n")
		fw = open(lconf.suppl_730_dir+"/"+so+".tmp", 'w')
		for i in range(lconf.lda_num_topics):
			fw.write('TOPIC:'+str(i)+'__'+lda.print_topic(i, topn=lconf.topn).encode("utf-8")+"\r\n")
		fw.close()
		fa.close()

		words2[so] = []

	####################
	# output
	####################
	for so in words2.keys():
		fa = open(lconf.suppl_730_dir+"/"+so+".txt", 'a')
		f = open(lconf.suppl_730_dir+"/"+so+".tmp", 'r')
		for line in f.readlines():
			line = line.rstrip()
			fa.write(line+"\r\n")
		f.close()
		fa.close()
		os.remove(lconf.suppl_730_dir+"/"+so+".tmp")

	# log
	fa = open("730.log", 'a')
	fa.write(rdp[0]+"\t"+str(lconf.limit_record4journal)+"\t"+str(i)+"\t"+str(len(words2))+"\t"+last_rawdata+"\r\n")
	fa.close()

	break	#test
