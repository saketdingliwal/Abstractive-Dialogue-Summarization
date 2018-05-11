import json
import re
import sys
import nltk
import pickle
import csv

def is_amp(word):
	arr = re.findall("&", word)
	if(len(arr)==0):
		return False
	else:
		print("AMP", word)
		return True

def is_special(word):
	arr = re.findall("\W.*\W", word)
	if(len(arr)==0):
		return False
	else:
		# print("SPECIAL", word)
		return True	

def clean_sent(sent):
	sent_arr = sent.split()
	if(">" in sent_arr[0]):
		return " "
	if("&gt;" in sent_arr[0]):
		return " "
	new_sent = []
	for word in sent.split():
		if(is_special(word)):
			continue
		elif(is_amp(word)):
			continue
		else:
			new_sent.append(word)

	return " ".join(new_sent)

with open('cont.pickle', 'rb') as handle:
    contractions = pickle.load(handle)

inputFile = sys.argv[1]
summaryFile = sys.argv[2]
output_folder = sys.argv[3]

corpus = json.load(open(inputFile))

lstno = []
conv = []
all_ids = []

for ele in corpus["root"]["thread"]:
	lstno.append(ele["listno"])
	fnl_sent = []
	sent_with_id = []
	ttl_len = 0
	for email in ele["DOC"]:
		name = email["From"].split()[0]
		if(isinstance(email["Text"]["Sent"], list)):
			for sent in email["Text"]["Sent"]:
				ttl_len += len(clean_sent(sent["#text"]).split())
				fnl_sent.append((name, clean_sent(sent["#text"])))
				sent_with_id.append((sent["-id"], clean_sent(sent["#text"])))
		else:
			ttl_len += len(clean_sent(sent["#text"]).split())
			fnl_sent.append((name, clean_sent(email["Text"]["Sent"]["#text"])))
			sent_with_id.append((sent["-id"], clean_sent(email["Text"]["Sent"]["#text"])))
	print(ttl_len)
	conv.append(fnl_sent)
	all_ids.append(sent_with_id)

data = json.load(open(summaryFile))

summ = []

for i in range(len(lstno)):
	for ele in data["root"]["thread"]:
		if(lstno[i]==ele["listno"]):
			temp_ele = ""
			for sent in ele["annotation"][0]["summary"]["sent"]:
				if "-link" in sent:
					links = sent["-link"]
					for evry in links.split(','):
						for lin in all_ids[i]:
							if (lin[0]==evry):
								temp_ele += "\n@highlight\n"
								temp_ele += lin[1]
			summ.append(temp_ele)
			break


for i, ele in enumerate(conv):

	myFile = open(output_folder + str(i) + ".csv", 'w', newline='')
	with myFile:
		fieldnames = ['speaker', 'pos']
		writer = csv.DictWriter(myFile, fieldnames=fieldnames, delimiter=':')
		writer.writeheader()
		for dia in ele:
			writer.writerow({'speaker' : dia[0], 'pos' : dia[1]})


	# print(len(ele.split()))
	filename = output_folder + str(i) + ".story"
	with open(filename, 'w') as writer:
		writer.write(summ[i])
