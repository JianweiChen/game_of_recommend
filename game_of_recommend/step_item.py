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

    def __init__(self, game):
        super().__init__(game)
    
    def real_run(self):
        
    
    @property
    def item_pool_is_full(self):
        return len(self.context.map_item) >= self.game.size_item_pool
    
    @property
    def item_pool_need_eliminate(self):
        return len(self.context.map_item) > self.game.size_item_pool
    
    def new_some_item(self):
        ctx = self.context
        for _ in range(self.game.size_new_item):
            item = Item()
            if item.tid not in ctx.map_item:
                ctx.map_item[item.tid] = item
