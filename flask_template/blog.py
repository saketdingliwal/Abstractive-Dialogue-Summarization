import json
import re
import nltk



connectors = [['anyway'], ['like'], ['right'], ['you', 'know'], ['fine'], ['now'], ['so'], ['I', 'mean'], ['good'], ['oh'], ['well'], ['as', 'I', 'say'], ['great'], ['okay'], ['mind', 'you'], ['for', 'a', 'start']]

# def get_connectors(sent):
# 	global connectors
# 	for conn in connectors:

def cln_word(word):
	if(word[-3:]=="\'ve"):
		return [word[:-3], 'have']
	elif(word[-2:]=="\'d"):
		return [word[:-2], ' had']
	elif(word[-2:]=="\'ll"):
		return [word[:-2], ' will']
	elif(word[-2:]=="\'m"):
		return [word[:-2], ' is']
	elif(word[-3:]=="\'re"):
		return [word[:-3], ' are']
	else:
		return [word]

def getspe(word):
	term = re.findall("\w*:", word)
	return term[0][:-1]

def getname(sent):
	mid_sent = []
	for word in sent.split():
		mid_sent.extend(cln_word(word))
	
	curr_name = "Someone"
	other_name = "Someone"
	for word in mid_sent:
		arr = re.findall("\w*:\w*", word)
		if(len(arr)==1):
			curr_name = getspe(word)
			other_name = curr_name

	
	new_sent = []
	for word in mid_sent:
		arr = re.findall("\w*:\w*", word)
		if(len(arr)==1):
			other_name = curr_name
			curr_name = getspe(word)
		elif(word=="I" or word=="i"):
			new_sent.append(curr_name)
		elif(word=="My" or word=="my"):
			new_sent.append(curr_name + "\'s")
		elif(word=="You" or word=="you"):
			new_sent.append(other_name)
		elif(word=="Your" or word=="your"):
			new_sent.append(other_name + "\'s")
		else:
			new_sent.append(word)
	return " ".join(new_sent)

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

corpus = json.load(open('blog_dataset/blog_data.json'))

conv = []

for ele in corpus:
	full_sent = getname(ele["Dialog"])
	print(full_sent)
	summ_sent = getsummary(ele["Summary"])
	# print(summ_sent)
	for sent in summ_sent.split('.'):
		if(len(sent.split())==0):
			continue
		full_sent += "\n@highlight\n" + " ".join(sent.split()) + '.'

	# for ind_sent in full_sent.split('.'):
	# 	tags = nltk.pos_tag(ind_sent.split())
	conv.append(full_sent)

for i, ele in enumerate(conv):
	print(len(ele.split()))
	filename = "folder/" + str(i) + ".story"
	with open(filename, 'w') as writer:
		print(ele)
		writer.write(ele)