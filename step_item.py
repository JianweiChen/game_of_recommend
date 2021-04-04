# coding=utf8

import os
import sys
import json
import pickle
import random
import string
import math
import time

from step import Step

class Item(object):
    
    def __init__(self, word_t):
        self.tid = hash(word_t) % 100_000_000
        self.word_t = word_t
    
    def __repr__(self):
        return "%s_%s" % (self.tid, self.word_t)

class StepItem(Step):

    def __init__(self, game, need_summary=False):
        super().__init__(game, need_summary)
    
    def real_run(self):
        
        self.new_some_item()
        while not self.item_pool_is_full:
            self.new_some_item()
        self.eliminate_item()
    
    # The parameter p means to start from top What percentage of 
    # the words to randomly generate the target word
    def random_1_word(self, p):
        k = int(len(self.context.list_rank_word) * p)
        list_word = self.context.list_rank_word[:k]
        assert len(list_word) > 0
        return random.choice(list_word)

    @property
    def item_pool_is_full(self):
        return len(self.context.map_item) >= self.game.size_item_pool
    
    @property
    def item_pool_need_eliminate(self):
        return len(self.context.map_item) > self.game.size_item_pool
    
    def new_some_item(self):
        ctx = self.context
        for _ in range(self.game.size_new_item):
            item = Item(
                self.random_1_word(self.game.rate_word_item)
            )
            if item.tid not in ctx.map_item:
                ctx.map_item[item.tid] = item
    
    # Because new items are added to the pool, some old items need to be eliminated randomly
    def eliminate_item(self):
        ctx = self.context
        count_eliminate = max(0, len(ctx.map_item) - self.game.size_item_pool)
        list_tid_eliminate = random.sample(list(ctx.map_item), count_eliminate)
        for tid in list_tid_eliminate:
            ctx.map_item.pop(tid)