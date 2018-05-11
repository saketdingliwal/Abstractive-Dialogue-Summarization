import sys
from collections import namedtuple
import csv
import glob
import os
import pickle

def get_utterances_from_file(dialog_csv_file, dialog_csv_filename):
    """Returns a list of DialogUtterances from an open file."""
    reader = csv.DictReader(dialog_csv_file)
    path = dialog_csv_filename.split("\\")
    return [_dict_to_dialog_utterance(du_dict, path[-1]) for du_dict in reader]

def get_utterances_from_filename(dialog_csv_filename):
    """Returns a list of DialogUtterances from an unopened filename."""
    with open(dialog_csv_filename, "r") as dialog_csv_file:
        return get_utterances_from_file(dialog_csv_file, dialog_csv_filename)

def get_data(data_dir):
    """Generates lists of utterances from each dialog file.

    To get a list of all dialogs call list(get_data(data_dir)).
    data_dir - a dir with csv files containing dialogs"""
    dialog_filenames = sorted(glob.glob(os.path.join(data_dir, "*.csv")))
    for dialog_filename in dialog_filenames:
        yield get_utterances_from_filename(dialog_filename)

DialogUtterance = namedtuple("DialogUtterance", ("act_tag", "speaker", "pos", "text", "fileName"))

PosTag = namedtuple("PosTag", ("token", "pos"))

def _dict_to_dialog_utterance(du_dict, dialog_csv_filename):
    """Private method for converting a dict to a DialogUtterance."""

    # Remove anything with
    for k, v in du_dict.items():
        if len(v.strip()) == 0:
            du_dict[k] = None

    # Extract tokens and POS tags
    if du_dict["pos"]:
        du_dict["pos"] = [
            PosTag(*token_pos_pair.split("/"))
            for token_pos_pair in du_dict["pos"].split()]
    du_dict["fileName"] = dialog_csv_filename
    return DialogUtterance(**du_dict)

print ('Argument count : ', len(sys.argv))
#exit if file name is not provided as command line argument
if len(sys.argv) != 4:
    print ('Please send file name as command line argument')
    exit(0)

trainDir = sys.argv[1]
devDir = sys.argv[2]
outputFile = sys.argv[3]

print ('trainDir : ', trainDir, ' devDir : ', devDir,' outputFile : ', outputFile)

# get all utterances
files_train = get_data(trainDir)
files_test = get_data(devDir)


contractions = {
"ain't": "am not ",
"aren't": "are not",
"can't": "cannot",
"can't've": "cannot have",
"'cause": "because",
"could've": "could have",
"couldn't": "could not",
"couldn't've": "could not have",
"didn't": "did not",
"doesn't": "does not",
"don't": "do not",
"hadn't": "had not",
"hadn't've": "had not have",
"hasn't": "has not",
"haven't": "have not",
"he'd": "he had",
"he'd've": "he would have",
"he'll": "he shall",
"he'll've": "he shall have",
"he's": "he has",
"how'd": "how did",
"how'd'y": "how do you",
"how'll": "how will",
"how's": "how is",
"i'd": "I would",
"i'd've": "I would have",
"i'll": "I shall",
"i'll've": "I shall have",
"i'm": "I am",
"i've": "I have",
"isn't": "is not",
"it'd": "it would",
"it'd've": "it would have",
"it'll": "it will",
"it'll've": "it will have",
"it's": "it is",
"let's": "let us",
"ma'am": "madam",
"mayn't": "may not",
"might've": "might have",
"mightn't": "might not",
"mightn't've": "might not have",
"must've": "must have",
"mustn't": "must not",
"mustn't've": "must not have",
"needn't": "need not",
"needn't've": "need not have",
"o'clock": "of the clock",
"oughtn't": "ought not",
"oughtn't've": "ought not have",
"shan't": "shall not",
"sha'n't": "shall not",
"shan't've": "shall not have",
"she'd": "she would",
"she'd've": "she would have",
"she'll": "she will",
"she'll've": "she will have",
"she's": "she is",
"should've": "should have",
"shouldn't": "should not",
"shouldn't've": "should not have",
"so've": "so have",
"so's": "so is",
"that'd": "that had",
"that'd've": "that would have",
"that's": "that is",
"there'd": "there would",
"there'd've": "there would have",
"there's": "there is",
"they'd": "they would",
"they'd've": "they would have",
"they'll": "they will",
"they'll've": "they will have",
"they're": "they are",
"they've": "they have",
"to've": "to have",
"wasn't": "was not",
"we'd": "we would",
"we'd've": "we would have",
"we'll": "we will",
"we'll've": "we will have",
"we're": "we are",
"we've": "we have",
"weren't": "were not",
"what'll": "what will",
"what'll've": "what will have",
"what're": "what are",
"what's": "what is",
"what've": "what have",
"when's": "when is",
"when've": "when have",
"where'd": "where did",
"where's": "where is",
"where've": "where have",
"who'll": "who will",
"who'll've": "who will have",
"who's": "who is",
"who've": "who have",
"why's": "why is",
"why've": "why have",
"will've": "will have",
"won't": "will not",
"won't've": "will not have",
"would've": "would have",
"wouldn't": "would not",
"wouldn't've": "would not have",
"y'all": "you all",
"y'all'd": "you all would",
"y'all'd've": "you all would have",
"y'all're": "you all are",
"y'all've": "you all have",
"you'd": "you would",
"you'd've": "you would have",
"you'll": "you will",
"you'll've": "you will have",
"you're": "you are",
"you've": "you have"
}

with open('cont.pickle', 'wb') as handle:
    pickle.dump(contractions,handle)


ignore_tags = ["b","%","fo_o_fw_by_bc","x","fc","bk","h","qy^d","bh","ad","^2","b^m","qo","qh","^h","ar","ng","br","no","fp","qrr","arp_nd","t3","o_co_cc","t1","bd","aap_am","^g","qw^d","fa","ft"]
answer_tags = ["ny","nn","na"]
question_tags = ["qy"]

replaced_by = {}
replaced_by["aa"] = "agreed ."
replaced_by["ba"] = "appreciated ."

i_list = ["i","me"]
i_list_poss = ["my"]
you_list = ["you"]
you_list_poss = ["your"]



opp_speaker = {}
opp_speaker["A"] = "B"
opp_speaker["B"] = "A"

def frame_ans(question_utter,dialogUtterance):
	article = question_utter.speaker +  " asked"
	if question_utter.pos:
		for posTag in question_utter.pos:
			article += (" " + posTag.token)
	if dialogUtterance.act_tag == "ny" or dialogUtterance.act_tag == "na":
		article += (" "+dialogUtterance.speaker + " agreed .")
	else:
		article += (" "+dialogUtterance.speaker + " disagreed .")
	return article	



article_list = []
for utterances in files_train:
	article = []
	lastspeaker = "X"
	question_utter = None
	for dialogUtterance in utterances:
		if dialogUtterance.act_tag in  ignore_tags:
			continue
		if dialogUtterance.act_tag in replaced_by:
			article.append(dialogUtterance.speaker)
			article.append(replaced_by[dialogUtterance.act_tag])
			continue
		if dialogUtterance.act_tag in question_tags:
			question_save = dialogUtterance
			continue
		if dialogUtterance.act_tag in answer_tags:
			if question_save == None:
				continue
			if not question_save.speaker == dialogUtterance.speaker:
				ans_string = frame_ans(question_save,dialogUtterance)
				article.append(ans_string)
				question_save = None
				continue
		if dialogUtterance.pos:
			for i in range(len(dialogUtterance.pos)):
				posTag = dialogUtterance.pos[i]
				next_pos = None
				new_token = posTag.token
				if not i==0 and ( dialogUtterance.pos[i-1].token.lower() == new_token.lower()) :
					print (dialogUtterance.pos[i-1].token.lower()," ",new_token.lower())
					continue
				if not i == (len(dialogUtterance.pos)-1):
					next_pos = dialogUtterance.pos[i+1]
				if next_pos and "\'" in next_pos.token:
					word = posTag.token
					word += next_pos.token
					if word.lower() in contractions:
						word = contractions[word.lower()]
						new_token = word
					else:
						word = posTag.token + " is"
						new_token = word
				if posTag.pos=="UH" or posTag.pos=="," or "\'" in posTag.token:
					continue
				if new_token.split()[0] in i_list:
					new_token = dialogUtterance.speaker + " "+ ' '.join(new_token.split()[1:])
				if new_token.split()[0] in i_list_poss:
					new_token = dialogUtterance.speaker + "'s "
				if new_token.split()[0] in you_list:
					new_token = opp_speaker[dialogUtterance.speaker] +" " + ' '.join(new_token.split()[1:])
				if new_token.split()[0] in you_list_poss:
					new_token = opp_speaker[dialogUtterance.speaker] + "'s "
				article.append(new_token)
			lastspeaker = dialogUtterance.speaker
	article = " ".join(article)
	article_list.append(article)
	
print (article_list[0])
# print (article_list[1])
# print (article_list[2])
