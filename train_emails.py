#coding: utf-8

# Carlos Interaminense
# Órion
# Caio Batista

import os
import sys
import csv

key_words_for_identify_spam = ["viagra", "vi@gra", "viagr@", "vi@gr@"]
key_words_exist_in_all_emails = ["subject:"]

#labels para identificar spams e hams
LABEL_SPAM = 0
LABEL_HAM = 1
all_words_in_spams = []
number_repeateds_words_in_spams = []

#cria hostogramas dos emails, a partir da frequencia das palavras mais repetidas nos spams.
#O primeiro elemento de cada histograma é a label dele, se é spam ou ham, de acordo com as variaveis supracitadas
def create_histograms(all_emails, topn_words, histograms):

	for i in range(len(all_emails)):
		l = []
		for j in range(len(topn_words) + 1):
			l.append(0)
		histograms.append(l)
	
	row = 0
	index =0
	for email in all_emails:
		col = 1
		flag = False

		for key_word in key_words_for_identify_spam:
			if key_word in email[1]:
				l = []
				n_max = max(number_repeateds_words_in_spams)
				l.append(email[0])
				for i in range(len(topn_words)):
					l.append(n_max)
				histograms[row] = l
				flag = True
			
		if flag:
			row+=1
			index+=1
			continue
		
		histograms[row][0] = email[0]
		for w in topn_words:
			if w in email[1]:
				histograms[row][col] = email[1][w]
			col +=1
		row+=1
		
		index+=1
	
#conta a frequencia das palavras no email
def count_repeated_words_in_email(email, label):
	repeated_words={}
	label_plus_repeated_words = ()
	for word in email:
		word = word.lower()
		if word in repeated_words:
			repeated_words[word]+=1
		else:
			repeated_words[word] = 1

		if word in all_words_in_spams:
			index = all_words_in_spams.index(word)
			number_repeateds_words_in_spams[index] += 1
		else:
			all_words_in_spams.append(word)
			number_repeateds_words_in_spams.append(1)
			

	label_plus_repeated_words=(label, repeated_words) 

	return label_plus_repeated_words

#para deixar tudo numa lista
def substitute_line_per_espace(email):
	email = email.split("\n")
	s = ""
	for i in email:
		s = s + i + " "
	return s

#só precisa no treinamento. As N (number_words) palavras mais repetidas nos spams
def words_more_repeatesd_in_spam(number_words, list_words, list_often):
	count = 0

	while(count < number_words):
		number_max = max(number_repeateds_words_in_spams)

		word = all_words_in_spams[number_repeateds_words_in_spams.index(number_max)]

		if(len(word) <= 3 or (word in key_words_exist_in_all_emails)):
			number_repeateds_words_in_spams.remove(number_max)
			all_words_in_spams.remove(word)
			continue

		count+=1	

		list_words.append(word)
		list_often.append(number_max)

		number_repeateds_words_in_spams.remove(number_max)

		all_words_in_spams.remove(word)

#caminho para a pasta de treinamento
path_train = sys.argv[1]
#numero de palavras que vamos considerar, pode ser um número fixo
#as N palavras mais repedidas nos spams
number_words_train = int(sys.argv[2])

dirs_train = os.listdir(path_train)

spams = os.listdir(path_train+"/spam/")
hams = os.listdir(path_train+"/ham/")


all_emails = []

print "read spams emails..."
for i in range(len(spams)):
	email_spam = spams[i]
	f = open(path_train + "/spam/" + email_spam)
	print "%d. %s" % (i+1, path_train + "/spam/" + email_spam)
	email_without_line = substitute_line_per_espace(f.read())
	extract_features_email = count_repeated_words_in_email(email_without_line.split(" "), LABEL_SPAM)	
	all_emails.append(extract_features_email)

print "read hams emails..."
for i in range(len(hams)):
	email_ham = hams[i]
	f = open(path_train + "/ham/" + email_ham)
	print "%d. %s" % (i+1,path_train + "/ham/" + email_ham)
	email_without_line = substitute_line_per_espace(f.read())
	extract_features_email = count_repeated_words_in_email(email_without_line.split(" "), LABEL_HAM)
	all_emails.append(extract_features_email)
list_words = []
list_often = []
words_more_repeatesd_in_spam(number_words_train, list_words, list_often)


histograms = []
create_histograms(all_emails, list_words, histograms)

#save histograms
with open("file.csv", "wb") as f:
    writer = csv.writer(f)
    wr = csv.writer(f, quoting=csv.QUOTE_ALL)
    wr.writerow(list_words)
    writer.writerows(histograms)

#save word mode repeateds
myfile = open("words.csv", 'wb')
wr = csv.writer(myfile, quoting=csv.QUOTE_ALL)
wr.writerow(list_words)
