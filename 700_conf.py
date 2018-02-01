##################################################
#	Configuration File
##################################################

# for 720, 730
suppl_720_dir = "../s720"	# dictionary directory
limit_dictionary = 100000	# use at least X records for dictionary
trained_datetime = "2018-01-01 00:00:00"
trained_period = 3			# show past X years

# for 730
limit_feature = 100		# use at least X records for feature of journals
topn = 20
lda_num_topics = 10
lda_alpha = 1.0

#####
# for 740
suppl_740_dir = "../s740"
output_740_file = "00010000.uni.cosine.tsv"

# To apply for your paper
input_file = ""				# When input_file is null, execution of research runs.
#input_file = "mypaper.txt"	# Wnen input_file is your text file (title, abstruct, etc.), application runs.

#####