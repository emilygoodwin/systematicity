from ruamel.yaml import YAML
from sentence import Sentence
from item import Item
from ident import Ident
import random
from random import randint
from utils import interpret, myprint
from sentencesampler import SentenceSampler
import pdb
import copy

yaml = YAML()
dev_split = 0.8

def get_nvlcoreset(blocka,blockb,mydict,test,itemtype,stepadded):
    '''
    Like get_bkg coreset, however, each item contains at least one novel word (novel noun or verb)
    Expects two ints, containing the block # for nouns and verbs
    a dict of previously-generated sentences 
    a boolean if the items are test or train items (if test, must generate neighbours)
    a string 'itemtype' which details the train/test condition (as explained in gen_blocks)

    get_nvlcoreset returns the dict, with additional entries
    Generates an inventory of nouns and verbs (including the 'novel' words - noun & verb)
    Generates a single core set, each item in that set has at least one novel noun or verb. 
    This single core set can be broken into four classes, fixing each of the positions in turn: 
        target noun, all nouns, verb, verb
        noun, target noun, verb, verb
        noun, noun, target verb, verb
        noun, noun, target verb, verb 
    Within each class, iterate over every way to combine the target with the other nouns & verbs
    Sample other filler words (quantifiers, adjectives, relative clauses) to create a sentence pair. 
    Checks for doubles; no elements of core set are already existing in dict
    Generates neighbouring sentences (if test == 1) and puts them all in mydict

    warning: if it cannot create a unique core set, because all possible sentence items with 
    a certain NNVV combo are created, it will hang (continue resampling forever). 
    Make sure you are not calling this too many times/asking for impossible number of coresets! 
    '''

    with open("config.yml", 'r') as ymlfile:
        cfg = yaml.load(ymlfile)

    nouncount = cfg['language']['nouncount']
    verbcount = cfg['language']['verbcount']
    quantifiers = cfg['language']['quantifiers']
    adjectives = cfg['language']['adjectives']
    RC = cfg['language']['RC']
    Neg = cfg['language']['Neg']
    R = ['|', '>', '<', 'v', '^', '#']

    nouns = []
    verbs = []

    for i in range(0,7):
        nouns.append("N"+str(blocka)+"."+ str(i))
        verbs.append("V"+str(blockb)+"."+ str(i))

    sampler = SentenceSampler(quantifiers, adjectives, Neg,
                              RC, R, nouns, verbs)

    schemes = [[["N"+str(blocka)+"."+str(3)], nouns, verbs, verbs], 
    [nouns, ["N"+str(blocka)+"."+str(3)], verbs, verbs], 
    [nouns, nouns, ["V"+str(blockb)+"."+str(3)], verbs], 
    [nouns,nouns, verbs, ["V"+str(blockb)+"."+str(3)]]]

    for each in schemes: 

        for Psub in each[0]:
            for Hsub in each[1]:
                for Pverb in each[2]:
                    for Hverb in each[3]:
                        if test == 0: 
                            if (('.3' in Psub) or ('.3' in Hsub)) and (('.3' in Pverb) or ('.3' in Hverb)): 
                                continue; 
                        while True:
                            item = sampler.sample_item(Psub, Hsub, Pverb, Hverb, test)
                            if item not in mydict:
                                break
                            else:
                                sampler.reset()
                        itemID = Ident().nextid
                        mydict[item.string()] = item.correct, itemID, test, itemtype, blocka, blockb, stepadded, []
                        if test == 1:
                            neighbors = []
                            neighbIDs = []
                            while True:
                                nitem = sampler.get_nbr(test)
                                if nitem:
                                    # check that the neighbor distance is actually 1
                                    assert item.distance(nitem) == 1
                                    if nitem.correct != item.correct:
                                        neighbors.append(nitem)
                                else:
                                    break
                            for n in neighbors:
                                #If neighbour already generated, already in the dict: look up its ID, 
                                #extend its list of neighbours, and the list for current test item 
                                if n.string() in mydict: 
                                    mydict[n.string()][7].append(mydict[item.string()][1])
                                    nID = mydict[n.string()][1]
                                    mydict[item.string()][7].append(nID)
                                else:
                                #Nbr not already generated: get an ID number for it, make a new entry in the dict
                                #give this entry one neighbour (the current test item) and give current test item nID 
                                    nID = Ident().nextid
                                    mydict[n.string()] = n.correct, nID, n.test, 'nbr', blocka, blockb, stepadded, [mydict[item.string()][1]]
                                    mydict[item.string()][7].append(nID)
                            

                            #additionally, get the transposed item and add it to the nbr list
                            transhyp = item.get_premise()
                            transprem = item.get_hypothesis()
                            transitem = Item(transprem, transhyp, interpret(transprem, transhyp), 1)
                            tID = Ident().nextid
                            mydict[transitem.string()] = transitem.correct, tID, 1, 'TTR', blocka, blockb, stepadded, [mydict[item.string()][1]]
                            mydict[item.string()][7].append(tID)

                        elif test == 2:
                            # splitting with dev, 80% time delete the item from mydict
                            if random.uniform(0,1) <= dev_split:
                                del mydict[item.string()]

                        
                        sampler.reset()

    # Statistics, feel free to remove this
    #print("All data generated completed")
    #print("Total dict entries : {}".format(len(mydict)))
    #print("All dict entries: "), [mydict[key] for key in mydict]
    #print mydict
    return mydict
    
def get_bkgcoreset(blocka,blockb,mydict,test,itemtype, stepadded):
    '''
    Expects two ints, containing the block # for nouns and verbs
    a dict of previously-generated sentences 
    a boolean if the items are test or train items (if test, must generate neighbours)
    a string 'itemtype' which details the train/test condition (as explained in gen_blocks)

    get_bkgcoreset returns the dict, with additional entries
    generates an inventory of nouns and verbs (without the 'novel' word, as this is background)
    Then generates a single core set of sentence pairs for the given noun & verb inventory.
    Iterates over every noun, noun, verb, verb combination in the given inventory, samples the other
    words (quantifiers, adjectives, relative clauses) to create a sentence pair. 
    Checks for doubles; no elements of core set are already existing in dict
    Generates neighbouring sentences (if test == 1) and puts them all in mydict

    warning: if it cannot create a unique core set, because all possible sentence items with 
    a certain NNVV combo are created, it will hang (continue resampling forever). 
    Make sure you are not calling this too many times/asking for impossible number of coresets! 
    '''


    with open("config.yml", 'r') as ymlfile:
        cfg = yaml.load(ymlfile)

    nouncount = cfg['language']['nouncount']
    verbcount = cfg['language']['verbcount']
    quantifiers = cfg['language']['quantifiers']
    adjectives = cfg['language']['adjectives']
    RC = cfg['language']['RC']
    Neg = cfg['language']['Neg']
    R = ['|', '>', '<', 'v', '^', '#']

    nouns = []
    verbs = []
    #As this is the background coreset, we do not wish to generate 
    #the novel word (in the middle of hierarchy; for us, #3)
    for i in range(0,3):
        nouns.append("N"+str(blocka)+"."+ str(i))
        verbs.append("V"+str(blockb)+"."+ str(i))
    for i in range(4,7):
        nouns.append("N"+str(blocka)+"."+ str(i))
        verbs.append("V"+str(blockb)+"."+ str(i))
    

    sampler = SentenceSampler(quantifiers, adjectives, Neg,
                              RC, R, nouns, verbs)
    

    #dictionary: key is item.string(), columns are: 
    #label, ID, test/train, itemtype(celltype, or nbr if neighbour), nounblock, verbblock, neighbour list 
    for Psub in nouns:
        for Hsub in nouns:
            for Pverb in verbs:
                for Hverb in verbs:
                    while True:
                        item = sampler.sample_item(Psub, Hsub, Pverb, Hverb, test)
                        if item not in mydict:
                            break
                        else:
                            sampler.reset()
                    mydict[item.string()] = item.correct, Ident().nextid, test, itemtype, blocka, blockb, stepadded, []
                    if test == 1:
                        neighbors = []
                        neighbIDs = []
                        while True:
                            nitem = sampler.get_nbr(test)
                            if nitem:
                                # check that the neighbor distance is actually 1
                                assert item.distance(nitem) == 1
                                neighbors.append(nitem)
                            else:
                                break
                        for n in neighbors:
                            #If neighbour already generated, already in the dict: look up its ID, 
                            #extend its list of neighbours, and the list for current test item 
                            if n.string() in mydict: 
                                mydict[n.string()][7].append(mydict[item.string()][1])
                                nID = mydict[n.string()][1]
                                mydict[item.string()][7].append(nID)
                            else:
                            #Nbr not already generated: get an ID number for it, make a new entry in the dict
                            #give this entry one neighbour (the current test item) and give current test item nID 
                                nID = Ident().nextid
                                mydict[n.string()] = n.correct, nID, n.test, 'nbr', blocka, blockb, stepadded, [mydict[item.string()][1]]
                                mydict[item.string()][7].append(nID)

                    elif test == 2:
                        # splitting with dev, 80% time delete the item from mydict
                        if random.uniform(0, 1) <= dev_split:
                            del mydict[item.string()]
                    
                    sampler.reset()

    # Statistics, feel free to remove this
    #print("All data generated completed")
    #print("Total dict entries : {}".format(len(mydict)))
    #print("All dict entries: "), [mydict[key] for key in mydict]
    #print mydict
    return mydict