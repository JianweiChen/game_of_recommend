# coding=utf8

class User(object):
    def __init__(self, word_a, word_b):
        self.uid = hash((word_a, word_b)) % 100_000_000
        self.word_a = word_a
        self.word_b = word_b
        self.prior_ctr = None
    
    def set_prior_ctr(self, ctr):
        self.prior_ctr = ctr
    
    def __repr__(self):
        return "%s_%s_%s" % (self.uid, self.word_a, self.word_b) 
    
    