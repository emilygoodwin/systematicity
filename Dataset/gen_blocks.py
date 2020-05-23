from ruamel.yaml import YAML 
from sentence import Sentence
from item import Item
from ident import Ident
import random
from random import randint
from utils import interpret, myprint
from sentencesampler import SentenceSampler
from coresetgenerators import get_bkgcoreset, get_nvlcoreset
import pdb
import copy
import argparse

dev_split = 0.8
yaml = YAML()

def gen_blocks(blockcount, trainintra, traincross, test_intraR, test_crossR, test_crossF, test_crossN, wug_count):
    """
    Builds a 2-d matrix BLOCKS w/ training & test scheme
    Each entry X, Y represents a potential cell to sample sentence pairs from:
    Nouns from block X, verbs from block Y
    Each cell has tuple:
    - first entry is train condition:
    If we do not wish to sample fromthis cell for train, entry is 0
    If we do wish to sample from this cell for train, entry is three letter string with 'train type'
        First letter: n (train)
        Second letter: in (intra block, nouns & verbs from the same block) or cr (cross block)
    - second entry is test condition
    If we do not wish to sample from this cell for test, entry is 0
    If we do wish to test on a sample of this cell, entry is a 3 letter string with 'test type':
        First letter: t (test)
        Second letter: i (intra block, nouns & verbs from same block) or c (cross block)
        Third letter: r (this cell will be sampled from for train)
                f (this cell will not be sampled from for train, the mirrored cell (across diagonal) will be, the two intra cells for nouns & verbs will be)
                n (this cell will not be sampled from for train, the mirrored cell (across diagonal) will not be, the two intra cells for nouns & verbs will be)
                v (this cell will not be sampled from for train, the mirrored cell (across diagonal) will not be, the two intra cells for nouns & verbs will not be)
    """

    #populate block matrix with training/test scheme: each cell has 2 digits
    #blocks[x][y] = train(y/no), test(y/no)


    #trains: 100 "nin" 90 "ncr " or "nc"
    #tests:  20  "tir" 10 "tcr"
    #        20  "tcf" 40 "tcn" + wugs
    blocks = [[[0,0] for inner in range(blockcount)] for outer in range(blockcount)]
    for b in range(trainintra):
        blocks[b][b][0] = 'nin'
    for b in range(traincross):
        blocks[b][b+3][0] = 'ncr'
    for b in range(test_intraR):
        blocks[b][b][1] = 'TIR'

    for b in range(traincross+1, traincross+1+test_crossN):
        blocks[b+4][b][1] = 'TCN'
    for b in range(test_crossR):
        blocks[b][b+3][1] = 'TCR'

    for b in range(blockcount-wug_count, blockcount):
        blocks[b][b][1] = 'TIW'

    return blocks

def gen_sets(mydict, blocks, blockcount, novels, test, stepadded):
    '''
    Expects a matrix with the test/train conditions,
    Loops over this matrix, samples coresets where appropriate.
    returns a dict with the testing and training data.

    Warning: You need to start by generating the test coresets,
    this minimizes collisions with neighbours (generated in test)
    and train items. If you sample for train first, items will
    collide with neighbours and there will be less to test on
    '''
    if novels == 0:
        for a in range(blockcount):
            for b in range(blockcount):
                if test == 1:
                    if blocks[a][b][1] != 0:
                        get_bkgcoreset(a,b,mydict,1,blocks[a][b][1], stepadded)
                        get_bkgcoreset(a,b,mydict,1,blocks[a][b][1], stepadded)
                        print("generated background test coresets for cell: " + str(a) + ',' + str(b))
                elif test == 0:
                    if blocks[a][b][0] != 0:
                        get_bkgcoreset(a,b, mydict,0,blocks[a][b][0], stepadded)
                        get_bkgcoreset(a,b, mydict,0,blocks[a][b][0], stepadded)
                        print("generated background train coresets for cell: " + str(a) + ',' + str(b))
                elif test == 2:
                    if blocks[a][b][0] != 0:
                        get_bkgcoreset(a,b, mydict,2,blocks[a][b][0], stepadded)
                        get_bkgcoreset(a,b, mydict,2,blocks[a][b][0], stepadded)
                        print("generated background dev coresets for cell: " + str(a) + ',' + str(b))
    else:
        for a in range(blockcount):
            for b in range(blockcount):
                if test == 1:
                    if blocks[a][b][1] != 0:
                        for i in range(novels):
                            get_nvlcoreset(a,b,mydict,1,blocks[a][b][1], stepadded)
                            get_nvlcoreset(a,b,mydict,1,blocks[a][b][1], stepadded)
                            print("generated novel test coresets for cell: " + str(a) + ',' + str(b))
                elif test == 0:
                    if blocks[a][b][0] != 0:
                        for i in range(novels):
                            get_nvlcoreset(a,b, mydict,0,blocks[a][b][0], stepadded)
                            get_nvlcoreset(a,b, mydict,0,blocks[a][b][0], stepadded)
                            print("generated novel train coresets for cell: " + str(a) + ',' + str(b))
                elif test == 2:
                    if blocks[a][b][0] != 0:
                        for i in range(novels):
                            get_nvlcoreset(a,b, mydict,2,blocks[a][b][0], stepadded)
                            get_nvlcoreset(a,b, mydict,2,blocks[a][b][0], stepadded)
                            print("generated novel dev coresets for cell: " + str(a) + ',' + str(b))
    return mydict

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("-c","--config", default='config.yml', type=str, help='Config file to generate the blocks')
    parser.add_argument("-s","--steps", default=0, type=int, help='max number of steps')
    #parser.add_argument('-l','--loc', default='/scratch/koustuvs/compositionality/', type=str)
    parser.add_argument('-l','--loc', default= '', type=str)
    args = parser.parse_args()


    with open(args.config, 'r') as ymlfile:
        cfg = yaml.load(ymlfile)
    blockcount = cfg['language']['blockcount']
    trainintra = cfg['traincells']['intrablock']
    traincross = cfg['traincells']['crossblock']
    test_intraR = cfg['testcells']['intrablock']
    test_crossR = cfg['testcells']['trained_crossblock']     #crossblock cells, trained
    test_crossF = cfg['testcells']['fliptrained_crossblock'] #crossblock cells, untrained, w/ trained mirrors/'twins'
    test_crossN = cfg['testcells']['untrained_crossblock']   #crossblock cells, untrained, flip untrained
    wug_count = cfg['testcells']['wug_count']     #crossblock cells XY where neither X nor Y has been crossed in train

    blocks = gen_blocks(blockcount, trainintra, traincross, test_intraR, test_crossR, test_crossF, test_crossN, wug_count)
    outfile = open("blocks.csv", "w")
    for a in blocks:
        for b in a:
            outfile.write(str(b)+ ',')
        outfile.write("\n")


    # construct test set- bckg and novel
    # this test set will remain the same for each step
    my_dict = {}
    my_dict = gen_sets(my_dict, blocks, blockcount, novels =0, test = 1, stepadded=0)
    my_dict = gen_sets(my_dict, blocks, blockcount, novels =1, test = 1, stepadded=0)

    for step in range(args.steps + 1):

        #construct training sets
        if step == 0:
            my_dict = gen_sets(my_dict, blocks, blockcount,novels =0, test = 0, stepadded=0)
            # add the dev set
            my_dict = gen_sets(my_dict, blocks, blockcount, novels=0, test=2, stepadded=0)
        else:
            my_dict = gen_sets(my_dict, blocks, blockcount,novels=1, test = 0, stepadded=step)
            # add the dev set
            my_dict = gen_sets(my_dict, blocks, blockcount, novels=1, test=2, stepadded=step)
        # save the full data
        myprint(my_dict, step, loc=args.loc)
        print("Done writing for step {}".format(step))
