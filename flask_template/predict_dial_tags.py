import sys
from collections import namedtuple
import csv
import glob
import os
import pycrfsuite
import pickle


specialCharacter = "!@#$%^*()_+~}{|:><?;-+"
my_dir=""

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
    dialog_filenames = (glob.glob(os.path.join(data_dir, "*.csv")))
    new_dialog_filenames = []
    for i in range(len(dialog_filenames)):
    	new_dialog_filenames.append(os.path.join(data_dir, str(i)+".csv"))

    for dialog_filename in new_dialog_filenames:
        yield get_utterances_from_filename(dialog_filename)

DialogUtterance = namedtuple("DialogUtterance", ("act_tag", "speaker", "pos", "text" ,"fileName"))

PosTag = namedtuple("PosTag", ("token", "pos"))

def _dict_to_dialog_utterance(du_dict, dialog_csv_filename):
    """Private method for converting a dict to a DialogUtterance."""

    # Remove anything with
    for k, v in du_dict.items():
        if len(v.strip()) == 0:
            du_dict[k] = None
    du_dict["act_tag"] = None
    du_dict["text"] = None
    # Extract tokens and POS tags
    if du_dict["pos"]:
        du_dict["pos"] = [
            PosTag(*token_pos_pair.split("/"))
            for token_pos_pair in du_dict["pos"].split()]
    du_dict["fileName"] = dialog_csv_filename
    return DialogUtterance(**du_dict)

def createFeatureList(files):
    xTrain = []
    fileNames = []
    for utterances in files:
        file = []
        first = True
        speaker = ''
        previous_label = ''
        for dialogUtterance in utterances:
            fileName = dialogUtterance.fileName
            feature = []
            if first:
                feature.append('1')
                feature.append('0')
                speaker = dialogUtterance.speaker
                first = False
            else:
                feature.append('0')
                if dialogUtterance.speaker == speaker:
                    feature.append('0')
                else:
                    feature.append('1')
                    speaker = dialogUtterance.speaker
            specialCharcterFlag = '0'
            if dialogUtterance.pos:
                for posTag in dialogUtterance.pos:
                    feature.append("TOKEN_"+posTag.token)
                    feature.append(posTag.token)
                    if posTag.token in specialCharacter:
                        specialCharcterFlag = '1'
                for posTag in dialogUtterance.pos:
                    feature.append("POS_"+posTag.pos)
            file.append(feature)
        xTrain.append(file)
        fileNames.append(fileName)
    return xTrain,fileNames



def frame_ans(question_utter,ques_string,dialogUtterance,ans_string,wh):
	article = question_utter.speaker +  " asked "
	article += ques_string
	# if question_utter.pos:
		# for posTag in question_utter.pos[:-1]:
			# article += (" " + posTag.token)
	if wh:
		article += (" and " + dialogUtterance.speaker + " replied ")
		# if dialogUtterance.pos:
			# for posTag in dialogUtterance.pos:
				# article += (" " + posTag.token)
		# article += " "
		article += ans_string
		print ("answer->")
		print (article)
		return article
	if dialogUtterance.act_tag == "ny" or dialogUtterance.act_tag == "na":
		article += (" "+dialogUtterance.speaker + " agreed .")
	else:
		article += (" "+dialogUtterance.speaker + " disagreed .")
	print ("answer->")
	print (article)
	return article	


def print_sentence(dialogue):
	sent =""
	if dialogue.pos:
		for posTag in dialogue.pos:
			sent += ' ' + posTag.token
		print (sent)
	return

def match(ques,ans):
	ques_words = []
	if ques.speaker == ans.speaker:
		return 0
	if ques.pos:
		for posTag in ques.pos:
			ques_words.append(posTag.token)
	else:
		return 0
	count_match = 0
	if ans.pos:
		for posTag in ans.pos:
			if posTag.token in ques_words:
				count_match+=1
	else:
		return 0
	return count_match/(1.0 * len(ques_words))




# print ('Argument count : ', len(sys.argv))
#exit if file name is not provided as command line argument

def run():
	testDir = my_dir + "csv/"
	outputDir = my_dir + "stories/"

	files_test = get_data(testDir)
	xTest, filenames_test = createFeatureList(files_test)

	tagger = pycrfsuite.Tagger()
	tagger.open(my_dir + 'baseline_model_new.crfsuite')

	yPred = [tagger.tag(xseq) for xseq in xTest]


	ignore_tags = ["b","%","fo_o_fw_by_bc","x","fc","bk","h","qy^d","bh","ad","^2","b^m","qo","^h","ar","ng","br","no","fp","qrr","arp_nd","t3","o_co_cc","t1","bd","aap_am","^g","qw^d","fa","ft"]
	answer_tags = ["ny","nn","na"]
	question_tags = ["qy"]
	question_wh = ["qw","qh"]

	replaced_by = {}
	replaced_by["aa"] = " agreed ."
	replaced_by["ba"] = " appreciated ."

	i_list = ["i","me"]
	i_list_poss = ["my"]
	you_list = ["you"]
	you_list_poss = ["your"]

	thresh_match = 0.3
	files_test = get_data(testDir)
	article_list = []
	for iterr_i,utterances in enumerate(files_test):
		article = []
		lastSpeaker = "X"
		currentSpeaker = "X"
		question_save = None
		wh_question = 0
		wh_question_save = None
		for iterr_j,dialogUtterance in enumerate(utterances):
			pos_string = ""
			if dialogUtterance.pos:
				for posTag in dialogUtterance.pos:
					if posTag.pos == "UH":
						continue
					new_token = posTag.token
					if posTag.token.lower() in i_list:
						new_token = dialogUtterance.speaker
					if posTag.token.lower() in i_list_poss:
						new_token = dialogUtterance.speaker + "\'s "
					if posTag.token.lower() in you_list:
						new_token = lastSpeaker
					if posTag.token.lower() in you_list_poss:
						new_token = lastSpeaker + "\'s "
					if posTag.token.lower() == "am":
						new_token = "is"
					pos_string += (" " + new_token)		
			if not dialogUtterance.speaker==currentSpeaker:
				lastSpeaker = currentSpeaker
				currentSpeaker = dialogUtterance.speaker
			if yPred[iterr_i][iterr_j] in ignore_tags:
				continue
			if yPred[iterr_i][iterr_j] in question_tags:
				question_save_string  = pos_string
				question_save = dialogUtterance
				continue
			if yPred[iterr_i][iterr_j] in question_wh:
				wh_question_save = dialogUtterance
				wh_question_save_string = pos_string
				wh_question = 1
				continue
			sent_formed = ""
			if wh_question > 0: 
				match_score = match(wh_question_save,dialogUtterance)
				wh_question +=1
				if match_score > thresh_match and wh_question < 10:
					ans_string = frame_ans(wh_question_save,wh_question_save_string,dialogUtterance,pos_string,1)
					sent_formed += (ans_string)
					wh_question = 0
					wh_question_save = None
			if sent_formed == "" and yPred[iterr_i][iterr_j] in replaced_by:
				sent_formed += dialogUtterance.speaker
				sent_formed += replaced_by[yPred[iterr_i][iterr_j]]
			if sent_formed == "" and yPred[iterr_i][iterr_j] in answer_tags:
				if question_save == None:
					continue
				if not question_save.speaker == dialogUtterance.speaker:
					ans_string = frame_ans(question_save,question_save_string,dialogUtterance,pos_string,0)
					sent_formed += ans_string
					question_save = None
			if sent_formed == "":
				sent_formed = pos_string
			article.append(sent_formed)
		article = " ".join(article)
		article_list.append(article)

	for i, ele in enumerate(article_list):
		# print(len(ele.split()))
		# filename = testDir + str(i) + ".story"
		# with open(filename, 'r') as reader:
		# 	data = reader.read()
		filename = outputDir + str(i) + ".story"
		with open(filename, 'w') as writer:
			writer.write(ele)
			# writer.write(data)


# print(article_list[0])