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
def morpheme(sentences):
	lemmatizer = nltk.stem.WordNetLemmatizer()
	symbols = ["'", '"', '`', '.', ',', '-', '!', '?', ':', ';', '(', ')']
	stopwords = nltk.corpus.stopwords.words('english')

	freq = {}
	for stc in sentences:
		tokens = nltk.word_tokenize(stc)
		for tkn in tokens:
			if tkn in stopwords + symbols:
				continue
			if tkn.strip().replace(".","",1).isdigit():
				continue
			if tkn.strip().replace(',',"",1).isdigit():
				continue
			tkn = tkn.encode("UTF-8")
			w = lemmatizer.lemmatize(tkn)
			if len(w) <= 1:
				continue
			freq.setdefault(w, 0)
			freq[w] += 1
	return freq


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


