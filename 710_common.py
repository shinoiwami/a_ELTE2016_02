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
def morpheme_list(ngram, sentences):
	lemmatizer = nltk.WordNetLemmatizer()
	stopwords = nltk.corpus.stopwords.words('english')
	pattern = re.compile("^['+-./=`*:\_]+")	# best
	patnum = re.compile("[0-9]+")
	
	list = []
	for stc in nltk.sent_tokenize(sentences):
		stc = stc.lower()
		tokens = nltk.word_tokenize(stc)
		
		# common
		for i in range(len(tokens)-1):
			if len(tokens[i]) <= 1:
				continue
			if tokens[i] in stopwords:
				continue
			if pattern.search(tokens[i]):
				continue
			if patnum.search(tokens[i]):
				continue
			wd = tokens[i]

			# bi-gram
			if ngram == "bi" and i+1 > len(tokens)-1:
				break
			if ngram == "bi":
				if len(tokens[i+1]) <= 1:
					continue
				if tokens[i+1] in stopwords:
					continue
				if pattern.search(tokens[i+1]):
					continue
				if patnum.search(tokens[i]):
					continue
				tokens[i+1] = lemmatizer.lemmatize(tokens[i+1])
				wd += " " + tokens[i+1]

			# tri-gram
			if ngram == "tri" and i+2 > len(tokens)-1:
				break
			if ngram == "tri":
				if len(tokens[i+2]) <= 1:
					continue
				if tokens[i+2] in stopwords:
					continue
				if pattern.search(tokens[i+2]):
					continue
				if patnum.search(tokens[i]):
					continue
				tokens[i+2] = lemmatizer.lemmatize(tokens[i+2])
				wd += " " + tokens[i+2]
	
			wd = lemmatizer.lemmatize(wd)
			list.append(wd)
			i += 1
	return list


def morpheme_freq(ngram, sentences):
	lemmatizer = nltk.WordNetLemmatizer()
	stopwords = nltk.corpus.stopwords.words('english')
	pattern = re.compile("^['+-./=`*:\_]+")	# best
	patnum = re.compile("[0-9]+")
	
	freq = {}
	for stc in nltk.sent_tokenize(sentences):
		stc = stc.lower()
		tokens = nltk.word_tokenize(stc)
		
		
		# common
		for i in range(len(tokens)-1):
			if len(tokens[i]) <= 1:
				continue
			if tokens[i] in stopwords:
				continue
			if pattern.search(tokens[i]):
				continue
			if patnum.search(tokens[i]):
				continue
			wd = tokens[i]

			# bi-gram
			if ngram == "bi" and i+1 > len(tokens)-1:
				break
			if ngram == "bi":
				if len(tokens[i+1]) <= 1:
					continue
				if tokens[i+1] in stopwords:
					continue
				if pattern.search(tokens[i+1]):
					continue
				if patnum.search(tokens[i]):
					continue
				tokens[i+1] = lemmatizer.lemmatize(tokens[i+1])
				wd += " " + tokens[i+1]
			
			# tri-gram
			if ngram == "tri" and i+2 > len(tokens)-1:
				break
			if ngram == "tri":
				if len(tokens[i+2]) <= 1:
					continue
				if tokens[i+2] in stopwords:
					continue
				if pattern.search(tokens[i+2]):
					continue
				if patnum.search(tokens[i]):
					continue
				tokens[i+2] = lemmatizer.lemmatize(tokens[i+2])
				wd += " " + tokens[i+2]

			wd = lemmatizer.lemmatize(wd)
			freq.setdefault(wd, 0)
			freq[wd] += 1
	return freq


# as memmo
def morpheme_freq_temp(sentences):
	lemmatizer = nltk.WordNetLemmatizer()
	symbols = ["'", '"', '`', '.', ',', '-', '!', '?', ':', ';', '(', ')', '/']
	stopwords = nltk.corpus.stopwords.words('english')
	pattern = re.compile("^[0-9'+-./=`]+")
	
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
			if pattern.search(tag[0]):
				continue
			w = lemmatizer.lemmatize(tag[0])
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


###  jaccard coefficient
def jaccard_coefficient(wordlist1, wordlist2):
	if len(wordlist1) == 0 or len(wordlist2) == 0:
		return 0.0
	cnt = 0.0
	for w in wordlist1:
		if w in wordlist2:
			cnt += 1.0
	sim = cnt / (len(wordlist1) + len(wordlist2) - cnt)
	return sim


###  dice coefficient
def dice_coefficient(wordlist1, wordlist2):
	if len(wordlist1) == 0 or len(wordlist2) == 0:
		return 0.0
	cnt = 0.0
	for w in wordlist1:
		if w in wordlist2:
			cnt += 1.0
	sim = 2 * cnt / (len(wordlist1) * len(wordlist2))
	return sim


###  simpson coefficient
def simpson_coefficient(wordlist1, wordlist2):
	if len(wordlist1) == 0 or len(wordlist2) == 0:
		return 0.0
	cnt = 0.0
	for w in wordlist1:
		if w in wordlist2:
			cnt += 1.0
	sim = cnt / min([len(wordlist1), len(wordlist2)])
	return sim


