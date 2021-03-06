#!/usr/bin/python
# -*- coding: utf-8 -*-

conf = __import__("000_conf")
lconf = __import__("700_conf")
lcommon = __import__("710_common")

import codecs
import MySQLdb
import os

from gensim import corpora


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
sql = u"SELECT rawdata_path FROM rawdata_control WHERE source = 'wos' AND entry_time >= '"+lconf.datetime_s_dictionary+u"' AND entry_time < '"+lconf.datetime_e_dictionary+u"' ORDER BY entry_time DESC;"
cursor.execute(sql)
rawdata_pathes = cursor.fetchall()
connector.commit()
cursor.close()

i = 0
words = []
check_ut = []
check_rdp = []
for rdp in rawdata_pathes:
	if rdp[0] in check_rdp:
		continue
	check_rdp.append(rdp[0])
	files = os.listdir(rdp[0])
	if i >= lconf.limit_dictionary:
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
				check_ut.append(ut)
				i += 1

				####################
				# morphological analysis
				####################
				text = " ".join([cell[header_map['TI']], cell[header_map['AB']], cell[header_map['ID']], cell[header_map['DE']]])
				words_tmp = lcommon.morpheme_list(lconf.ngram_dictionary, text.decode('utf-8'))
				words.append(words_tmp)
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

	####################
	# make dictionary
	####################
	# make output dir
	if not os.path.exists(lconf.suppl_720_dir):
		os.mkdir(lconf.suppl_720_dir)

	dictionary = corpora.Dictionary(words)
	dictionary.filter_extremes(no_below=2, no_above=0.80, keep_n=1000000)
	dictionary.save_as_text(lconf.suppl_720_dir+"/_dictionary.txt")

	# log
	fa = open("720.log", 'a')
	fa.write(lconf.ngram_dictionary+"\t"+rdp[0]+"\t"+str(i)+"\t"+str(len(open(lconf.suppl_720_dir+"/_dictionary.txt").readlines()))+"\r\n")
	fa.close()
