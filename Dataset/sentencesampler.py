import copy
import random
from sentence import Sentence
from item import Item
from utils import interpret
class SentenceSampler:
    def __init__(self, quant, adj, neg, rc, rel, nouns, verbs):
        """
        Expects quantifiers, adjectives, negations, relation clauses,
        relations, nouns and verbs in a list. 
        """
        self.quant = quant
        self.adj = adj
        self.neg = neg
        self.rc = rc
        self.rel = rel
        self.nouns = nouns
        self.verbs = verbs
        self.reset()

    def sample_item(self, n1, n2, v1, v2, test):
        """
        Sample a sentence from a given combination of nouns and verbs.
        Given a noun-noun-verb-verb combination, sample randomly from
        the remaining classes
        :param n1: first noun
        :param n2: second noun
        :param v1: first verb
        :param v2: second verb
        :test : flag to show that it belongs to test
        """
        self.selection = {'noun_1': n1, 'noun_2': n2,
                          'verb_1': v1, 'verb_2': v2}
        for key, val in self.vocab.items():
            if 'noun' not in key and 'verb' not in key:
                self.selection[key] = random.choice(self.vocab[key])
            self.vocab[key].remove(self.selection[key])
        # selection ready, now create the sentence
        return self.select_item(test)

    def select_item(self, test):
        """
        Expects a selection dictionary (with vocab) and returns an item
        """
        premise = Sentence(
                self.selection['quant_1'], self.selection['adj_1'],
                self.selection['noun_1'], "", self.selection['rc_1'],
                self.selection['neg_1'], self.selection['verb_1']
                )
        hypothesis = Sentence(
                self.selection['quant_2'], self.selection['adj_2'],
                self.selection['noun_2'], "", self.selection['rc_2'],
                self.selection['neg_2'], self.selection['verb_2']
                )
        item = Item(premise, hypothesis, interpret(premise, hypothesis), test)
        return item

    def get_nbr(self, test):
        """
        Iteratively enumerate a neighbour 1-edit distance from self, and return True if found.
        The idea is to remove from each choice when we enumerate a neighbour (eventually we run out, all neighbours generated)
        """
        for key, val in self.vocab.items():
            if len(val) > 0:
                old_selection = self.selection[key]
                self.selection[key] = random.choice(self.vocab[key])
                self.vocab[key].remove(self.selection[key])
                item = self.select_item(test)
                # revert old selection
                self.selection[key] = old_selection
                return item
        return False

    def reset(self):
        """
        Reset state
        """
        self.vocab = {
                'quant_1':  copy.deepcopy(self.quant),
                'quant_2':  copy.deepcopy(self.quant),
                'adj_1':    copy.deepcopy(self.adj),
                'adj_2':    copy.deepcopy(self.adj),
                'neg_1':    copy.deepcopy(self.neg),
                'neg_2':    copy.deepcopy(self.neg),
                'rc_1':     copy.deepcopy(self.rc),
                'rc_2':     copy.deepcopy(self.rc),
                'noun_1':   copy.deepcopy(self.nouns),
                'noun_2':   copy.deepcopy(self.nouns),
                'verb_1':   copy.deepcopy(self.verbs),
                'verb_2':   copy.deepcopy(self.verbs)
                }
        # current selection
        self.selection = {}