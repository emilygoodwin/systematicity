from sentence import Sentence

class Item:
    @staticmethod
    def parse_training_item(string):
        #print "Parsing: " + string.strip()
        fields=string.strip().split('\t')
        prem=Sentence.parse(fields[1])
        hyp=Sentence.parse(fields[2])
        return(Item(prem,hyp,fields[0],fields[0],False))
    
    def __init__(self, premise, hypothesis, correct, test):
        self.premise = premise
        self.hypothesis = hypothesis
        self.correct = correct
        self.test = test
        
    def hash_key(self):
        return(str(self.premise)+str(self.hypothesis)+str(self.correct)+str(self.label)+str(self.test))
        
    def get_premise(self):
        return(self.premise)

    def get_hypothesis(self):
        return(self.hypothesis)
        
    def distance(self, other):
        return(self.premise.distance(other.premise) +
        self.hypothesis.distance(other.hypothesis))

    def csv(self):
        return (str(self.premise)+","+str(self.hypothesis)+","+str(self.correct)+","+ str(self.test))

    def string(self):
        return (str(self.premise)+","+str(self.hypothesis))