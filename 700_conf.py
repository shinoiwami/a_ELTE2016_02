##################################################
#	Configuration File
##################################################

# for 730, 740
ngram = "uni"					# "uni", "bi", "tri"

# for 720
ngram_dictionary = "tri"		# "uni", "bi", "tri"
limit_dictionary = 1000000		# use at least X records for dictionary (max: 1000000)
datetime_s_dictionary = "2017-10-01 00:00:00"
datetime_e_dictionary = "2018-01-01 00:00:00"
suppl_720_dir = "../s720_3"		# dictionary directory

# for 730
limit_record4journal = 3000000	# use at least X records for feature of journals
datetime_s_trained = "2017-01-01 00:00:00"
#datetime_e_trained = "2018-01-01 00:00:00"
datetime_e_trained = "2017-12-17 00:00:00"

suppl_730_dir = "../s720"		# dictionary directory
dictionary_file = "_dictionary.txt"
topn = 1000
lda_num_topics = 1
lda_alpha = 1.0

#####
# for 740
limit_test = 1000
similarity = "cosine"			# "cosine", "jaccard", "dice", "simpson"
sim_word_count = 1000
suppl_740_dir = "../s740"
output_740_file = "uni.00100000.cosine.1000.tsv"
	# naming rule of connecting with period: ngram, limit_record4journal, similarity

# To apply for your paper
input_file = ""					# When input_file is null, execution of research runs.
#input_file = "mypaper.txt"		# Wnen input_file is your text file (title, abstruct, etc.), application runs.

#####