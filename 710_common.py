#!/usr/bin/python
# -*- coding: utf-8 -*-

import math
import nltk
import os
import re
import shutil
import sys
import time


############################################################
### morphological analysis
def morpheme_freq(sentences):
	lemmatizer = nltk.WordNetLemmatizer()
	symbols = ["'", '"', '`', '.', ',', '-', '!', '?', ':', ';', '(', ')', '/']
	stopwords = nltk.corpus.stopwords.words('english')

	freq = {}
	for stc in nltk.sent_tokenize(sentences):
		stc = stc.lower()
		tokens = nltk.word_tokenize(stc)
		tagged = nltk.pos_tag(tokens)
		
		for tag in tagged:
			if tag[0] in stopwords + symbols:
				continue
			if tag[0].strip().replace(".","",1).isdigit():
				continue
			if tag[0].strip().replace(',',"",1).isdigit():
				continue
			w = lemmatizer.lemmatize(tag[0])
			if len(w) <= 1:
				continue
			freq.setdefault(w, 0)
			freq[w] += 1
	return freq


def morpheme_list(sentences):
	lemmatizer = nltk.WordNetLemmatizer()
	symbols = ["'", '"', '`', '.', ',', '-', '!', '?', ':', ';', '(', ')', '/']
	stopwords = nltk.corpus.stopwords.words('english')
	
	list = []
	for stc in nltk.sent_tokenize(sentences):
		stc = stc.lower()
		tokens = nltk.word_tokenize(stc)
		tagged = nltk.pos_tag(tokens)
		
		for tag in tagged:
			if tag[0] in stopwords + symbols:
				continue
			if tag[0].strip().replace(".","",1).isdigit():
				continue
			if tag[0].strip().replace(',',"",1).isdigit():
				continue
			w = lemmatizer.lemmatize(tag[0])
			if len(w) <= 1:
				continue
			list.append(w)
	return list


############################################################
###  cosine similarity
def cosine_similarity(wordlist1, wordlist2):
	if len(wordlist1) == 0 or len(wordlist2) == 0:
		return 0.0
	cnt = 0.0
	for w in wordlist1:
		if w in wordlist2:
			cnt += 1.0
	sim = cnt / (math.sqrt(len(wordlist1)) * math.sqrt(len(wordlist2)))
	return sim


