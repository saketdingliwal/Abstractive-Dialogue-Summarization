import json
import re
import nltk
from nltk.tokenize import sent_tokenize
from nltk.tokenize import word_tokenize
from nltk.corpus import words as eng_words
import csv
import sys
import pickle

def getspe(word):
	term = re.findall("\w*:", word)
	return term[0][:-1]

def cln_word(word):
	if '/' in word:
		return []
	if '\'' in word:
		if word.lower() in contractions:
			return contractions[word.lower()].split()
	punc = [',', '.', '?', ';']
	if(word[-1] in punc):
		return [word[:-1], word[-1]]
	else:
		return [word]

def getname(sent):
	mid_sent = []
	for word in sent.split():
		mid_sent.append(word)
	
	curr_name = "Someone"
	other_name = "Someone"
	for word in mid_sent:
		arr = re.findall("\w*:\d*-", word)
		if(len(arr)==1):
			other_name = curr_name
			curr_name = getspe(word)
			if(other_name!="Someone"):
				break

	fnl_ans = []
	new_sent = []
	for word in mid_sent:
		arr = re.findall("\w*:\d*-", word)
		if(len(arr)==1):
			if(len(new_sent)>0):
				for ele in (" ".join(new_sent)).split('.'):
					if(len(ele.split())>0):
						fnl_ans.append((curr_name, ele))
			other_name = curr_name
			curr_name = getspe(word)
			new_sent = []
		else:
			new_sent.extend(cln_word(word))
	return fnl_ans

def getsummary(sent):
	words = sent.split()
	ans = []
	for word in words[3:]:
		if(word=="----------"):
			break
		if(word=="\\n"):
			continue
		if(word=="\\r"):
			continue
		ans.append(word)
	return " ".join(ans)

def pos_sent(tags):
	ans = ""
	for ele in tags:
		ans += ele[0]
		ans += "/"
		ans += ele[1]
		ans += " "
	return " ".join(ans.split())


with open('cont.pickle', 'rb') as handle:
    contractions = pickle.load(handle)

json_file = sys.argv[1]
output_folder = sys.argv[2]
corpus = json.load(open(json_file))

conv = []

for ele in corpus:
	full_data = getname(ele["Dialog"])
	summ_sent = getsummary(ele["Summary"])

	whole_data = []
	for spea, senten in full_data:
		tags = nltk.pos_tag(senten.split())
		whole_data.append((spea, pos_sent(tags)))

	full_sent = ""

	for sent in summ_sent.split('.'):
		if(len(sent.split())==0):
			continue
		full_sent += "\n@highlight\n" + " ".join(sent.split()) + '.'
	conv.append((whole_data, full_sent))

for i, ele in enumerate(conv):
	# print(len(ele.split()))
	filename = output_folder + str(i) + ".story"
	with open(filename, 'w') as writer:
		writer.write(ele[1])

	myFile = open(output_folder + str(i) + ".csv", 'w', newline='')
	with myFile:
		fieldnames = ['speaker', 'pos']
		writer = csv.DictWriter(myFile, fieldnames=fieldnames)
		writer.writeheader()
		for i, dia in enumerate(ele[0]):
			writer.writerow({'speaker' : dia[0], 'pos' : dia[1] + " ./."})
