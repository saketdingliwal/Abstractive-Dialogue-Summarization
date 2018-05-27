import sys
import csv
import nltk
import pickle
import glob
import os


my_dir = ""
punc = ['.', '?', ';', '!']
def pos_tagged(sent):
	tags = nltk.pos_tag(sent.split())
	ans = ""
	for ele in tags:
		ans += ele[0]
		ans += "/"
		ans += ele[1]
		ans += " "
	return " ".join(ans.split())

def cln_word(word,contractions):
	if '/' in word:
		return []
	if '\'' in word:
		if word.lower() in contractions:
			return contractions[word.lower()].split()
	if(word[-1] in punc):
		return [word[:-1], word[-1]]
	else:
		return [word]


def run():
	data = []
	with open(my_dir + 'cont.pickle', 'rb') as handle:
		contractions = pickle.load(handle)
	with open(my_dir + "0.csv", 'r') as file:
		abc = csv.DictReader(file,delimiter=':')
		for row in abc:
			new_sent = []
			if row['pos']:
				for ele in row['pos'].split():
					new_sent.extend(cln_word(ele,contractions))
					if len(new_sent) > 0 and new_sent[len(new_sent)-1] in punc:
						data.append((row['speaker'], " ".join(new_sent)))
						new_sent = []
						iterr = 0
				if len(new_sent) > 0:
					data.append((row['speaker'], " ".join(new_sent)))
		with open(my_dir + "csv/0.csv", 'w', newline='') as file:
			fieldnames = ['speaker', 'pos']
			writer = csv.DictWriter(file, fieldnames=fieldnames)
			writer.writeheader()
			for ele in data:
				writer.writerow({'speaker': ele[0], 'pos': pos_tagged(ele[1])})
	return 
