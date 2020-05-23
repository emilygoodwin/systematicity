#!/usr/bin/env python
#encoding: UTF-8

from itertools import product
from operator import itemgetter
from collections import defaultdict
from collections import Counter
from sentence import Sentence
from item import Item
import random
import pdb
import os
import re


#Interpretation function:
def interpret(p, h):
    FOR = "<"
    REV = ">"
    NEG = "^"
    ALT = "|"
    COV = "v"
    EQ = "="
    INDY = "#"
    UNK = "?"


    JOINTABLE = {  # Replaced UNK with INDY to match Emy's table
        EQ:  {EQ: EQ,  FOR: FOR, REV: REV, NEG: NEG,  ALT: ALT, COV: COV, INDY: INDY, INDY: INDY},
        FOR: {EQ: FOR, FOR: FOR, REV: INDY, NEG: ALT,  ALT: ALT, COV: INDY, INDY: INDY,  INDY: INDY},
        REV: {EQ: REV, FOR: INDY, REV: REV, NEG: COV,  ALT: INDY, COV: COV, INDY: INDY,  INDY: INDY},
        NEG: {EQ: NEG, FOR: COV, REV: ALT, NEG: EQ,   ALT: REV, COV: FOR, INDY: INDY, INDY: INDY},
        ALT: {EQ: ALT, FOR: INDY, REV: ALT, NEG: FOR,  ALT: INDY, COV: FOR, INDY: INDY,  INDY: INDY},
        COV: {EQ: COV, FOR: COV, REV: INDY, NEG: REV,  ALT: REV, COV: INDY, INDY: INDY,  INDY: INDY},
        INDY: {EQ: INDY, FOR: INDY, REV: INDY, NEG: INDY, ALT: INDY, COV: INDY, INDY: INDY,  INDY: INDY},
        UNK: {EQ: UNK, FOR: UNK, REV: UNK, NEG: UNK,  ALT: UNK, COV: UNK, INDY: UNK,  UNK: UNK},
    }

    #Set up vocabulary, Lexical relationships:

    relatives = ['', 'that hum', 'that sing']
    relatives_matrix = [
        [EQ,    REV,    REV,    REV], #''
        [FOR,   EQ,     REV,    REV],   #'that hum'
        [FOR,   FOR,    EQ,     REV],   #'that sing'
        [FOR,   FOR,    FOR,    EQ]#'that solo'
    ]

    dets = ['all', 'some']
    det_matrix = [
        # all   not_all some    no      most    not_most two    lt_two  three
        # lt_three
        [EQ,    NEG,    FOR,    ALT,    FOR,    ALT,     INDY,  INDY,   INDY,   INDY],  # all
        [NEG,   EQ,     COV,    REV,    COV,    REV,     INDY,  INDY,   INDY,   INDY],  # not_all
        [REV,   COV,    EQ,     NEG,    REV,    COV,     REV,   COV,    REV,    COV],  # some
        [ALT,   FOR,    NEG,    EQ,     ALT,    FOR,     ALT,   FOR,    ALT,    FOR],  # no
        [REV,   COV,    FOR,    ALT,    EQ,     NEG,     INDY,  INDY,   INDY,   INDY],  # most
        [ALT,   FOR,    COV,    REV,    NEG,    EQ,      INDY,  INDY,   INDY,   INDY],  # not_most
        [INDY,  INDY,   FOR,    ALT,    INDY,   INDY,    EQ,    NEG,    REV,    COV],  # two
        [INDY,  INDY,   COV,    REV,    INDY,   INDY,    NEG,   EQ,     ALT,    FOR],  # lt_two
        [INDY,  INDY,   FOR,    ALT,    INDY,   INDY,    FOR,   ALT,    EQ,     NEG],  # three
        [INDY,  INDY,   COV,    REV,    INDY,   INDY,    COV,   REV,    NEG,    EQ]    # lt_three
        ]
    negs = ['', 'not']
    negs_matrix = [
        #''     not
        [EQ,    2],     #'' in first position
        [1, 3]       #"not" first position
        ]

    adjectives = ['', 'rose', 'red']

    lexicon = {
        ('', ''):       EQ,
        ('', 'rose'):   REV,
        ('rose', ''):   FOR,
        ('rose', 'rose'): EQ,
        ('', 'red'):    REV,
        ('red', ''):    FOR,
        ('red', 'red'): EQ,
        ('rose', 'red'): FOR,
        ('red', 'rose'): REV
        }

    for i, j in product(range(len(negs)), range(len(negs))):
        lexicon[(negs[i], negs[j])] = negs_matrix[i][j]

    for i, j in product(range(len(dets)), range(len(dets))):
        lexicon[(dets[i], dets[j])] = det_matrix[i][j]

    for i, j in product(range(len(relatives)), range(len(relatives))):
        lexicon[(relatives[i], relatives[j])] = relatives_matrix[i][j]


    #decompose tree
    det = (p.quantifier, h.quantifier)
    adj = (p.adjective, h.adjective)
    noun = (p.noun, h.noun)
    relative = (p.relative, h.relative)
    neg = (p.negation, h.negation)
    verb = (p.verb, h.verb)

    #get noun relations
    if p.noun[-1] == h.noun[-1]:
        nounrelation = EQ
    elif p.noun[-1] > h.noun[-1]:
        nounrelation = FOR
    elif p.noun[-1] < h.noun[-1]:
        nounrelation = REV
    else:
        print("Could not find relation between nouns: " + str(noun))

    if p.verb[-1] == h.verb[-1]:
        verbrelation = EQ
    elif p.verb[-1] > h.verb[-1]:
        verbrelation = FOR
    elif p.verb[-1] < h.verb[-1]:
        verbrelation = REV
    else:
        print("Could not find relation between verbs: " + str(verb))


    #define the relationship between NPs
    if lexicon.get(relative) == EQ:
        if nounrelation == EQ:
            nprelation = EQ
        elif nounrelation == FOR:
            nprelation = FOR
        elif nounrelation == REV:
            nprelation = REV
        elif nounrelation == INDY:
            nprelation = INDY
        else:
            print("Could not find relation between Nouns: " + str(noun))

    elif lexicon.get(relative) == FOR:
        if nounrelation == EQ:
            nprelation = FOR
        elif nounrelation == FOR:
            nprelation = FOR
        elif nounrelation == REV:
            nprelation = INDY
        else:
            print("Could not find relation between Nouns: " + str(noun))

    elif lexicon.get(relative) == REV:
        if nounrelation == EQ:
            nprelation = REV
        elif nounrelation == FOR:
            nprelation = INDY
        elif nounrelation == REV:
            nprelation = REV
        else:
            print("Could not find relation between Nouns: " + str(noun))
    else:
        print("Could not find relation between Relative Clauses: " + str(rc))

    #define the relationship between APs
    if lexicon.get(adj) == EQ:
        if nprelation == EQ:
            aprelation = EQ
        elif nprelation == FOR:
            aprelation = FOR
        elif nprelation == REV:
            aprelation = REV
        elif nprelation == INDY:
            aprelation = INDY
        else:
            print("Can't find AP relation: " + str(adj))
    elif lexicon.get(adj) == FOR:
        if nprelation == EQ:
            aprelation = FOR
        elif nprelation == FOR:
            aprelation = FOR
        elif nprelation == REV:
            aprelation = INDY
        elif nprelation == INDY:
            aprelation = INDY
        else:
            print("Can't find AP relation: " + str(adj))
    elif lexicon.get(adj) == REV:
        if nprelation == EQ:
            aprelation = REV
        elif nprelation == FOR:
            aprelation = INDY
        elif nprelation == REV:
            aprelation = REV
        elif nprelation == INDY:
            aprelation = INDY
        else:
            print("Can't find AP relation: " + str(adj))
    else:
        print("help: nounmod?")

#define the relationship between VPS

    if lexicon.get(neg) == EQ:          #nonegation
        if verbrelation == FOR:
            vprelation = FOR
        elif verbrelation == REV:
            vprelation = REV
        elif verbrelation == ALT:
            vprelation = ALT
        elif verbrelation == EQ:
            vprelation = EQ
        else:
            print("can't find verb relation: " + str(verb))
    elif lexicon.get(neg) == 3:          #neg in both sentences
        if verbrelation == FOR:
            vprelation = REV
        elif verbrelation == REV:
            vprelation = FOR
        elif verbrelation == ALT:
            vprelation = COV
        elif verbrelation == EQ:
            vprelation = EQ
        else:
            print("can't find verb relation: " + str(verb))

    elif lexicon.get(neg) == 1:          #neg in position 1
        if verbrelation == FOR:
            vprelation = COV
        elif verbrelation == REV:
            vprelation = ALT
        elif verbrelation == ALT:
            vprelation = REV
        elif verbrelation == EQ:
            vprelation = NEG
        else:
            print("can't find verb relation: " + str(verb))
    elif lexicon.get(neg) == 2:          #neg in position 2
        if verbrelation == FOR:
            vprelation = ALT
        elif verbrelation == REV:
            vprelation = COV
        elif verbrelation == ALT:
            vprelation = FOR
        elif verbrelation == EQ:
            vprelation = NEG
        else:
            print("can't find verb relation: " + str(verb))
    else:
        print("can't find negation relation: " + str(neg))

#define the relationship between Sentences

    if det == ("some", "some"):
        if aprelation == EQ:
            if vprelation == EQ:
                return EQ
            if vprelation == FOR:
                return FOR
            if vprelation == REV:
                return REV
            if vprelation == NEG:
                return COV
            if vprelation == ALT:
                return INDY
            if vprelation == COV:
                return COV
            if vprelation == INDY:
                return INDY

        elif aprelation == FOR:
            if vprelation == EQ:
                return FOR
            if vprelation == FOR:
                return FOR
            if vprelation == REV:
                return INDY
            if vprelation == NEG:
                return COV
            if vprelation == COV:
                return COV
            if vprelation == ALT:
                return INDY
            if vprelation == INDY:
                return INDY
            else:
                "Np: FOR; VP: ?"

        elif aprelation == REV:
            if vprelation == EQ:
                return REV
            if vprelation == FOR:
                return INDY
            if vprelation == REV:
                return REV
            if vprelation == NEG:
                return COV
            if vprelation == COV:
                return COV
            if vprelation == ALT:
                return INDY ##used to be cov?
            if vprelation == INDY:
                return INDY
            else:
                "NP: FOR; VP: ?"

        elif aprelation == INDY:
            if vprelation == EQ:
                return INDY
            if vprelation == FOR:
                return INDY
            if vprelation == REV:
                return INDY
            if vprelation == NEG:
                return INDY
            if vprelation == COV:
                return INDY
            if vprelation == ALT:
                return INDY
            if vprelation == INDY:
                return INDY
            else:
                "NP: FOR; VP: ?"

    elif det == ("some", "all"):
        if aprelation == FOR:
            if vprelation == EQ:
                return REV
            if vprelation == FOR:
                return INDY
            if vprelation == REV:
                return REV
            if vprelation == NEG:
                return ALT
            if vprelation == ALT:
                return ALT
            if vprelation == COV:
                return INDY
            if vprelation == INDY:
                return INDY

        elif aprelation == REV:
            if vprelation == EQ:
                return REV
            if vprelation == FOR:
                return INDY
            if vprelation == REV:
                return REV
            if vprelation == NEG:
                return COV
            if vprelation == ALT:
                return INDY
            if vprelation == COV:
                return COV ##changed from INDY
            if vprelation == INDY:
                return INDY

        elif aprelation == EQ:
            if vprelation == EQ:
                return REV
            if vprelation == FOR:
                return INDY
            if vprelation == REV:
                return REV
            if vprelation == NEG:
                return NEG
            if vprelation == ALT:
                return ALT
            if vprelation == COV:
                return NEG
            if vprelation == INDY:
                return INDY

        elif aprelation == INDY:
            if vprelation == EQ:
                return INDY
            if vprelation == FOR:
                return INDY
            if vprelation == REV:
                return INDY
            if vprelation == NEG:
                return INDY
            if vprelation == ALT:
                return INDY
            if vprelation == COV:
                return INDY
            if vprelation == INDY:
                return INDY

    elif det == ("all", "some"):
        if aprelation == FOR:
            if vprelation == EQ:
                return FOR
            if vprelation == FOR:
                return FOR
            if vprelation == REV:
                return INDY
            if vprelation == NEG:
                return COV
            if vprelation == ALT:
                return INDY
            if vprelation == COV:
                return COV ##changed from INDY
            if vprelation == INDY:
                return INDY

        elif aprelation == REV:
            if vprelation == EQ:
                return FOR
            if vprelation == FOR:
                return FOR
            if vprelation == REV:
                return INDY
            if vprelation == NEG:
                return ALT
            if vprelation == ALT:
                return ALT
            if vprelation == COV:
                return INDY
            if vprelation == INDY:
                return INDY

        elif aprelation == EQ:
            if vprelation == EQ:
                return FOR
            if vprelation == FOR:
                return FOR
            if vprelation == REV:
                return INDY
            if vprelation == NEG:
                return NEG
            if vprelation == ALT:
                return ALT
            if vprelation == COV:
                return COV ##
            if vprelation == INDY:
                return INDY

        elif aprelation == INDY:
            if vprelation == EQ:
                return INDY
            if vprelation == FOR:
                return INDY
            if vprelation == REV:
                return INDY
            if vprelation == NEG:
                return INDY
            if vprelation == ALT:
                return INDY
            if vprelation == COV:
                return INDY
            if vprelation == INDY:
                return INDY
    elif det == ("all", "all"):
        if aprelation == EQ:
            if vprelation == EQ:
                return EQ
            elif vprelation == FOR:
                return FOR
            elif vprelation == REV:
                return REV
            elif vprelation == NEG:
                return ALT
            elif vprelation == ALT:
                return ALT
            elif vprelation == COV:
                return INDY
            elif vprelation == INDY:
                return INDY
            elif vprelation == UNK:
                print('warning: unclear relation')
        elif aprelation == FOR:
            if vprelation == EQ:
                return REV
            elif vprelation == FOR:
                return INDY
            elif vprelation == REV:
                return REV
            elif vprelation == NEG:
                return ALT
            elif vprelation == ALT:
                return ALT
            elif vprelation == COV:
                return INDY
            elif vprelation == INDY:
                return INDY
            elif vprelation == UNK:
                print('warning: unclear relation')
        elif aprelation == REV:
            if vprelation == EQ:
                return FOR
            elif vprelation == FOR:
                return FOR
            elif vprelation == REV:
                return INDY
            elif vprelation == NEG:
                return ALT
            elif vprelation == ALT:
                return ALT
            elif vprelation == COV:
                return INDY
            elif vprelation == INDY:
                return INDY
            elif vprelation == UNK:
                print('warning: unclear relation')
        elif aprelation == INDY:
            if vprelation == EQ:
                return INDY
            elif vprelation == FOR:
                return INDY
            elif vprelation == REV:
                return INDY
            elif vprelation == NEG:
                return INDY
            elif vprelation == ALT:
                return INDY
            elif vprelation == COV:
                return INDY
            elif vprelation == INDY:
                return INDY
            elif vprelation == UNK:
                print('warning: unclear relation')


def sample_item(quantifiers, adjectives, Psub, Hsub, RC, Neg, Pverb, Hverb, test):
    premise = Sentence(random.choice(quantifiers), random.choice(adjectives), Psub, "", random.choice(RC), random.choice(Neg), Pverb)
    hypothesis = Sentence(random.choice(quantifiers), random.choice(adjectives), Hsub, "",  random.choice(RC), random.choice(Neg), Hverb)
    item = Item(premise, hypothesis, interpret(premise, hypothesis), test)
    return(item)


def split_sents(recs, path, dt):
    s1 = []
    s2 = []
    labels = []
    for rec in recs:
        a,b,c = rec.split('\t')
        s1.append()
        s2.append(re.sub(' +', ' ', c.replace('(', '').replace(')','')))
        labels.append(a)
    with open(os.path.join(path, 's1.{}'.format(dt)),'w') as fp:
        fp.write('\n'.join(s1))
    with open(os.path.join(path, 's2.{}'.format(dt)),'w') as fp:
        fp.write('\n'.join(s2))
    with open(os.path.join(path, 'labels.{}'.format(dt)),'w') as fp:
        fp.write('\n'.join(labels))

def reformat(sent):
    return ' '.join(filter(None, [p.split(' ')[-1] for p in sent.split(')')]))

def myprint(mydict, stepnumber, loc='/steps/', split=0.8):
    save_path = os.path.join(loc, 'step_{}'.format(stepnumber))
    if not os.path.exists(save_path):
        os.mkdir(save_path)
    # outfile = open("all_data.csv", "w")
    outfile = open(os.path.join(save_path, "all_data.csv"),'w')
    outfile.write("item,label,ID,test,type,nounblock,verbblock,stepadded,neighbourlist,\n")#,MinTrainingLabels\n")
    outfile_id = 0
    clean_data = {
            'train': {'s1': [],'s2': [],'labels': [], 'ids': []},
            'test': {'s1': [],'s2': [],'labels': [], 'ids': []},
            'dev': {'s1': [],'s2': [],'labels': [], 'ids': []}
    }
    for key in mydict:
        outfile.write(key + ',' +
            str(mydict[key][0]) + ',' +
            str(mydict[key][1]) + ',' +
            str(mydict[key][2]) + ',' +
            str(mydict[key][3]) + ',' +
            str(mydict[key][4]) + ',' +
            str(mydict[key][5]) + ',' +
            str(mydict[key][6]) + ',' +
            str(mydict[key][7]) + "\n")
        outfile.flush()
        hyp_prem = key.split(',')
    #     if mydict[key][2] == 1:
    #         clean_data['test']['s1'].append(reformat(hyp_prem[0]))
    #         clean_data['test']['s2'].append(reformat(hyp_prem[1]))
    #         clean_data['test']['labels'].append(reformat(mydict[key][0]))
    #         clean_data['test']['ids'].append(str(outfile_id))
    #     elif mydict[key][2] == 0:
    #         clean_data['train']['s1'].append(reformat(hyp_prem[0]))
    #         clean_data['train']['s2'].append(reformat(hyp_prem[1]))
    #         clean_data['train']['labels'].append(reformat(mydict[key][0]))
    #         clean_data['train']['ids'].append(str(outfile_id))
    #     else:
    #         clean_data['dev']['s1'].append(reformat(hyp_prem[0]))
    #         clean_data['dev']['s2'].append(reformat(hyp_prem[1]))
    #         clean_data['dev']['labels'].append(reformat(mydict[key][0]))
    #         clean_data['dev']['ids'].append(str(outfile_id))
    #     outfile_id += 1

    # for dt, vals in clean_data.items():
    #     for flt, fltv in vals.items():
    #         with open(os.path.join(save_path, "{}.{}".format(flt, dt)),
    #                                                             'w') as fp:
    #             print("Writing {}.{} - {} lines".format(flt, dt, len(fltv)))
    #             fp.write('\n'.join(fltv))
    print("saving done.")
