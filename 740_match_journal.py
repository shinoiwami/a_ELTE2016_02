#!/usr/bin/python
# -*- coding: utf-8 -*-


conf = __import__("000_conf")
wos = __import__("020_wos")
lconf = __import__("700_conf")
lcommon = __import__("710_common")

import MySQLdb
import math
import nltk
import os
import random
import re
import sys
import time


############################################################
# read impact factor
impact_factor = {}
f = open("./700_JournalHomeGrid.csv", 'r')
linedmy = f.readline()
line1st = f.readline()
for line in f.readlines():
	line = line.rstrip()
	cell = line.split(',')
	if cell[1] == "":
		continue
	if cell[-3].strip().replace(".","",1).isdigit():
		score = float(cell[-3].strip())
	else:
		score = 0.0
	impact_factor[cell[1].strip().lower()] = score
f.close()


############################################################
# Get test data
############################################################
test_data = {}
test_info = {}
if lconf.input_file == "":
	# MySQL connector open
	fp = open(conf.auth, 'r')
	auth = fp.readline().rstrip().split(':')
	fp.close()
	connector = MySQLdb.connect(host="localhost", db="rawdata_control", user=auth[0], passwd=auth[1], charset="utf8")

	# test data
	cursor = connector.cursor()
	sql = u"SELECT rawdata_path FROM rawdata_control WHERE source = 'wos' AND entry_time >= '"+lconf.datetime_e_trained+u"' ORDER BY entry_time ASC;"
	cursor.execute(sql)
	rawdata_pathes = cursor.fetchall()
	connector.commit()
	cursor.close()

	i = 0
	check_ut = []
	check_rdp = []
	for rdp in rawdata_pathes:
		if rdp[0] in check_rdp:
			continue
		check_rdp.append(rdp[0])
		files = os.listdir(rdp[0])
		if i >= lconf.limit_test:
			break

		for file in files:
			if i >= lconf.limit_test:
				break
			if ".tsv" not in file:
				continue
		
			flag = 0
			header_map = {}
			f = open(rdp[0]+"/"+file, 'r')
			for line in f.readlines():
				if i >= lconf.limit_test:
					break
				
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
					if i % 100 == 0:
						print "test data", i
				
					####################
					# morphological analysis
					####################
					test_data[ut] = lcommon.morpheme_freq(lconf.ngram, " ".join([cell[header_map['TI']], cell[header_map['AB']], cell[header_map['ID']], cell[header_map['DE']]]))
					test_info[ut] = [cell[header_map['AU']], cell[header_map['TI']], cell[header_map['SO']].lower()]
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


# For application
else:
	f = open(input_file, 'r')
	for line in f.readlines():
		line = line.rstrip()
		test_data[ut] = lcommon.morpheme_freq(lconf.ngram, " ".join(line))
		test_info[ut] = ["Me", "TBD", "TBD"]
	f.close()



############################################################
# Match test data and journal data
############################################################
# make output dir
if not os.path.exists(lconf.suppl_740_dir):
	os.mkdir(lconf.suppl_740_dir)
fw = open(lconf.suppl_740_dir+"/"+lconf.output_740_file, 'w')

for ut in test_data.keys():
	i = 0
	j = 0

	sim = {}
	files = os.listdir(lconf.suppl_730_dir)
	for file in files:
		if ".txt" not in file:
			continue
		if "_dictionary" in file:
			continue

		# extract journal name
		name = file.split('.')
		so = name[0]

		trained_data = {}
		f = open(lconf.suppl_730_dir+"/"+file, 'r')
		for line in f.readlines():
			line = line.rstrip()
			lda_line = line.split('__')
			lda_cell = lda_line[1].split('+')
			for lc in lda_cell:
				lc = lc.strip()
				lda_data = lc.split('*')
				if len(lda_data) < 2:
					continue
				trained_data.setdefault(lda_data[1], 0.0)
				if trained_data[lda_data[1]] == 0.0:
					trained_data[lda_data[1]] = float(lda_data[0])

		# calc similarity
		sorted_trained = []
		for k, v in sorted(trained_data.items(), key=lambda x:x[1], reverse=True):
			sorted_trained.append(k)
		sorted_trained = sorted_trained[0:lconf.sim_word_count-1]
		if lconf.similarity == "jaccard":
			sim_tmp = lcommon.jaccard_coefficient(test_data[ut].keys(), sorted_trained)
		elif lconf.similarity == "dice":
			sim_tmp = lcommon.dice_coefficient(test_data[ut].keys(), sorted_trained)
		elif lconf.similarity == "simpson":
			sim_tmp = lcommon.simpson_coefficient(test_data[ut].keys(), sorted_trained)
		else:	# "cosine"
			sim_tmp = lcommon.cosine_similarity(test_data[ut].keys(), sorted_trained)
		
		i += 1
		if sim_tmp > 0.0:
			sim[so] = sim_tmp
			j += 1

	# output
	output = ut + "\t" + test_info[ut][0] + "\t" + test_info[ut][1] + "\t" + test_info[ut][2]
	for so, sc in sorted(sim.items(), key=lambda x:x[1], reverse=True):
		output += "\t" + so + ":" + str(sc)

	output += "\r\n"
	fw.write(output)

	if int(random.random()*100) % 100 == 0:
		print "all", i, "sim_count", j

fw.close()

