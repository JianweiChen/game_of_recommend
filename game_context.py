# coding=utf8
import os
import sys
import random
import logging

class GameContext(object):
    
    def __init__(self, hyper_param):
        
        self.hyper_param = hyper_param

        self.user_map = dict()
        self.item_map = dict()

        self.word_paragraph_position_map = dict()
        self.rank_word_list = []
        self.item_word_set = set()
        self.paragraph_id_queue = []

        # recommend
        self.dedup_set = set()

        self.loop_count = 0

        # corpus build
        self.built_corpus_name_set = set()
        self.buffer_word_list = []

        # dump and restore
        self.from_context_restore = False

    def get_preclk_example_path(self):
        name = 'preclk_example_loop_%04d.example.txt' % self.loop_count
        return os.path.join(self.hyper_param.k_example_path, name)

    def is_dup(self, uid, tid):
        key = '%s_%s' % (uid, tid)
        if key in self.dedup_set:
            return True
        return False

    def info(self, message, caller=None):
        if not caller:
            logging.info("%s loop=%s" % (message, self.loop_count))
        else:
            logging.info("%s loop=%s class=%s " % (message, self.loop_count, caller.__class__))
        

    def debug(self, message, caller=None):
        if not caller:
            logging.debug("%s loop=%s" % (message, self.loop_count))
        else:
            logging.debug("%s loop=%s class=%s " % (message, self.loop_count, caller.__class__))

    def get_random_word(self, n, r=0.3):
        assert len(self.rank_word_list) >= n
        k = int(len(self.rank_word_list) * r)
        result_word_list = random.sample(self.rank_word_list[:k], n)
        return result_word_list

