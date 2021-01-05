import os
import json
from sentence import Sentence
from item import Item
import re

def get_pairedItems():
	TCN = {}
	WUG = {}
	IdToStr = {}

	a = json.load(open('meta_data.json'))
	##I can't figure out why, but a is a dict with one entry (a nested dict, where the keys are actually sentences)
	#so we have to un-nest it: 
	for key in a: 
		StrToId= a[key]
		break
	#then build a dict to handle the reverse pointing: 
	for pair in StrToId: 
		IdToStr[StrToId[pair]] = pair


	with open('format_out.jsonl') as fp: 
		for line in fp:
			d = json.loads(line.rstrip())
			atup = IdToStr[d['PairA'][0]], IdToStr[d['PairA'][1]]
			bpairlist = d['PairB']
			acorrect = d['PairAcorrectlabel']
			apredict = d['PairApredictedlabel']
			bcorrect = d['PairBcorrectlabel']
			bpredict = d['PairBPredictedlabel']
			Atype = d['PairAtesttype']
			apair = get_item(atup, acorrect)
			if Atype == 'TCN':
				for each in zip(bpairlist, bcorrect, bpredict):
					btup = IdToStr[each[0][0]], IdToStr[each[0][1]]		
					bpair = get_item(btup, each[1])
			 		TCN[(apair.string(), bpair.string())] = acorrect, apredict, each[1], each[2], apair.diff(bpair)
			if (Atype == 'TIW') | (Atype == 'TCW'):
				for each in zip(bpairlist, bcorrect, bpredict):
					btup = IdToStr[each[0][0]], IdToStr[each[0][1]]
					bpair = get_item(btup, each[1])
					WUG[((apair.string(), bpair.string()))] =  acorrect, apredict, each[1], each[2], apair.diff(bpair)

	myprint('tcn', TCN)
	myprint('wug', WUG)


def myprint(name, mydict):
	outfile = open(os.path.join("", name + "tests_paired.csv"),'w')
	outfile.write("pairAprem, pairAhyp, pairBprem, pairBhyp, Acorrect,Apredicted,Bcorrect,Bpredicted, in, out, diff," + "\n") 

	for key in mydict: 
		outfile.write(key[0] + ', ' +	
			key[1] + ', ' +	
			str(mydict[key][0]) + ', ' +  
			str(mydict[key][1]) + ', ' + 
			str(mydict[key][2]) + ', ' + 
			str(mydict[key][3]) + ', ' + 
			str(mydict[key][4]) + ', ' + "\n")
	return

def get_item(tup, correct): 
	prem = tup[0].replace(")", '')
	hypo = tup[1].replace(")", '')
	prem = prem.replace("u'", '')
	hypo = hypo.replace("u'", '')
	prem = re.split(r'\(\w+', prem)
	hypo = re.split(r'\(\w+', hypo)
	prem = Sentence(prem[2], prem[3], prem[4], prem[5], prem[6], prem[7], prem[8])
	hypo = Sentence(hypo[2], hypo[3], hypo[4], hypo[5], hypo[6], hypo[7], hypo[8])
	pair = Item(prem, hypo, correct, 1)
	return(pair)

if __name__ == '__main__':
	get_pairedItems()