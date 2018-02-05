##################################################
#	Configuration File
##################################################

# for 730, 740
ngram = "uni"					# "uni", "bi", "tri"

# for 720
ngram_dictionary = "tri"		# "uni", "bi", "tri"
limit_dictionary = 100000		# use at least X records for dictionary (max: 100000)
datetime_dictionary = "2018-01-01 00:00:00"
period_dictionary = 1				# show past X years
suppl_720_dir = "../s720_3"		# dictionary directory

# for 730
limit_record4journal = 1000000	# use at least X records for feature of journals
datetime_trained = "2018-01-01 00:00:00"
period_trained = 1				# show past X years

suppl_730_dir = "../s720"		# dictionary directory
dictionary_file = "_dictionary.00100000.txt"
topn = 100
lda_num_topics = 1
lda_alpha = 1.0

#####
# for 740
limit_test = 1000
similarity = "cosine"			# "cosine", "jaccard", "dice", "simpson"
suppl_740_dir = "../s740"
output_740_file = "uni.00001000.cosine.tsv"
	# naming rule of connecting with period: ngram, limit_record4journal, similarity

# To apply for your paper
input_file = ""					# When input_file is null, execution of research runs.
#input_file = "mypaper.txt"		# Wnen input_file is your text file (title, abstruct, etc.), application runs.

#####