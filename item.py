# coding=utf8

class Item(object):
    def __init__(self, word_t):
        self.tid = hash(word_t) % 100_000_000
        self.word_t = word_t
    
    def __repr__(self):
        return '%s_%s' % (self.tid, self.word_t)