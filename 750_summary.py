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
import re
import shutil
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
# Get result data
############################################################
print "n-gram, record_count, similarity, test_count, ratio, max_rank, min_rank, max_score, min_score"

distribution = {}
files = os.listdir(lconf.suppl_740_dir)
for file in files:
	if ".tsv" not in file:
		continue

	# extract journal name
	name = file.split('.')

	(m, n) = (0, 0)
	(max_rank, min_rank) = (0, 0)
	(max_score, min_score) = (0.0, 0.0)
	f = open(lconf.suppl_740_dir+"/"+file, 'r')
	for line in f.readlines():
		line = line.rstrip()
		cell = line.split('\t')
		n += 1

		for l in range(4, len(cell)-1):
			rank = l - 3
			so = re.sub(r'[/]+', '', cell[3])
			if so+":" in cell[l]:
				score = cell[l].split(':')
				if float(score[1]) == 0.0:
					break
				
				m += 1

				if max_rank == 0 or max_rank > rank:
					max_rank = rank
				if min_rank == 0 or min_rank < rank:
					min_rank = rank

				if max_score == 0 or max_score > float(score[1]):
					max_score = float(score[1])
				if min_score == 0 or min_score < float(score[1]):
					min_score = float(score[1])

				distribution.setdefault(rank, 0)
				distribution[rank] += 1

				break

	ratio = m / float(n)
	print name[0], name[1], name[2], n, ratio, max_rank, min_rank, max_score, min_score
	print distribution


