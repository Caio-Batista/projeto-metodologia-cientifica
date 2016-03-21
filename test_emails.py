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
LABEL_SPAM = "spam"
LABEL_HAM = "ham"

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
		col = 0
		flag = False

		#caso exista alguma palavra no email que está na lista de identificar spams...
		for key_word in key_words_for_identify_spam:
			if key_word in email[1]:
				l = []
				#teria que salvar as frequencias das palavras tb, no treinamento, como nao salvel, vai esse numero magico msm
				n_max = 50
				for i in range(len(topn_words)):
					l.append(n_max)
				l.append(email[0])
				histograms[row] = l
				flag = True
			
		if flag:
			row+=1
			index+=1
			continue
		
		histograms[row][-1] = email[0]
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


	label_plus_repeated_words=(label, repeated_words) 

	return label_plus_repeated_words

#para deixar tudo numa lista
def substitute_line_per_espace(email):
	email = email.split("\n")
	s = ""
	for i in email:
		s = s + i + " "
	return s

def read_file_csv(file_name_csv):
	l = []
	with open(file_name_csv, 'rb') as f:
	    reader = csv.reader(f)
	    l = list(reader)
	return l

#caminho para a pasta de treinamento
path_test = sys.argv[1]
file_name_csv = "words.csv"

list_words = read_file_csv(file_name_csv)[0]


dirs_test = os.listdir(path_test)

spams = os.listdir(path_test+"/spam/")
hams = os.listdir(path_test+"/ham/")


all_emails = []

print "read spams emails..."
for i in range(len(spams)):
	email_spam = spams[i]
	f = open(path_test + "/spam/" + email_spam)
	print "%d. %s" % (i+1, path_test + "/spam/" + email_spam)
	email_without_line = substitute_line_per_espace(f.read())
	extract_features_email = count_repeated_words_in_email(email_without_line.split(" "), LABEL_SPAM)	
	all_emails.append(extract_features_email)

print "read hams emails..."
for i in range(len(hams)):
	email_ham = hams[i]
	f = open(path_test + "/ham/" + email_ham)
	print "%d. %s" % (i+1,path_test + "/ham/" + email_ham)
	email_without_line = substitute_line_per_espace(f.read())
	extract_features_email = count_repeated_words_in_email(email_without_line.split(" "), LABEL_HAM)
	all_emails.append(extract_features_email)


histograms = []
create_histograms(all_emails, list_words, histograms)

#save histograms
with open("file_test.csv", "wb") as f:
    writer = csv.writer(f)
    wr = csv.writer(f, quoting=csv.QUOTE_ALL)
    writer.writerows(histograms)

