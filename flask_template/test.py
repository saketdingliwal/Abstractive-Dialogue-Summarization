import json
import re

def is_email(word):
	arr = re.findall("\w*@\w*\.\w*", word)
	if(len(arr)==0):
		return False
	else:
		print("EMAIL", word)
		return True

def is_url(word):
	arr = re.findall("\w*\.\w*\.\w*", word)
	if(len(arr)==0):
		return False
	else:
		print("URL", word)
		return True

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
	if(len(sent_arr)==1):
		return " "
	if(sent_arr[0]==">"):
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

corpus = json.load(open('corpus.json'))

lstno = []
conv = []


for ele in corpus["root"]["thread"]:
	lstno.append(ele["listno"])
	fnl_sent = ""
	for email in ele["DOC"]:
		name = email["From"].split()[0]
		fnl_sent += name + " said that "
		if(isinstance(email["Text"]["Sent"], list)):
			for sent in email["Text"]["Sent"]:
				fnl_sent += clean_sent(sent["#text"]) + " "
		else:
			fnl_sent += clean_sent(email["Text"]["Sent"]["#text"]) + " "
	conv.append(fnl_sent)


data = json.load(open('summary.json'))

for i in range(len(lstno)):	
	for ele in data["root"]["thread"]:
		if(lstno[i]==ele["listno"]):
			for sent in ele["annotation"][0]["summary"]["sent"]:
				conv[i] += "\n@highlight\n"
				conv[i] += sent["#text"]
			break

for i, ele in enumerate(conv):
	print(len(ele.split()))
	filename = "folder/" + str(i) + ".story"
	with open(filename, 'w') as writer:
		print(ele)
		writer.write(ele)