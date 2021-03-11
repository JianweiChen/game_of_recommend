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


class User(object):
    def __init__(self, word_a, word_b):
        self.uid = hash((word_a, word_b)) % 100_000_000
        self.word_a = word_a
        self.word_b = word_b
        self.map_impression = dict()
        self.map_click = dict()
        self.map_pay = dict()
        # Filled in the recommended step, read and cleared in the example step
        self.list_tid_recommend = []
    
    def __repr__(self):
        return '{}_{}_{}'.format(self.uid, self.word_a, self.word_b)

class StepUser(Step):

    def __init__(self, game, need_summary=False):
        super().__init__(game, need_summary)
    
    # Different from paragraph and item, the user does not need to be fully recruited in the 
    # first round of operation. Each round is recruited with a fixed quota, and there is no 
    # specific limit on how much can be left.
    def real_run(self):
        if not len(self.context.map_user):
            self.load_user_pkl()
        max_solicit_success = max(self.game.size_new_user, self.game.size_user_pool - len(self.context.map_user))
        solicit_success = 0
        for _ in range(self.game.size_solicit_attemp):
            user_or_none = self.solicit()
            if user_or_none:
                user = user_or_none
                self.context.map_user[user.uid] = user
                solicit_success += 1
                if solicit_success >= max_solicit_success:
                    break
        self.context.map_summary['solicit_success'] = solicit_success   
        self.eliminate_user()
        self.dump_user_pkl()
    
    def load_user_pkl(self):
        if os.path.exists(self.game.path_user_pkl):
            with open(self.game.path_user_pkl, 'rb') as f:
                self.context.map_user = pickle.load(f)
    
    def dump_user_pkl(self):
        with open(self.game.path_user_pkl, 'wb') as fw:
            pickle.dump(self.context.map_user, fw)

    # If the solicitation is successful, return the user, otherwise return None
    def solicit(self):
        ctx = self.context
        judge = self.game.judge_manager
        word_a, word_b = self.random_2_word(self.game.rate_word_user)
        user = User(word_a, word_b)
        if user.uid in ctx.map_user:
            return None
        # Browse some items to decide whether to stay
        list_tid = list(ctx.map_item)
        k = int(len(list_tid) * self.game.rate_solicit_browse)
        list_tid = random.sample(list_tid, k)
        for tid in list_tid:
            item = ctx.map_item[tid]
            if judge.judge_click(user, item):
                # print(user, item, judge.judge_pay(user, item))
                return user
        return None

    # The parameter p means to start from top What percentage of 
    # the words to randomly generate the target word
    def random_2_word(self, p):
        k = int(len(self.context.list_rank_word) * p)
        list_word = self.context.list_rank_word[:k]
        assert len(list_word) > 0
        two_word = random.sample(list_word, 2)
        return two_word[0], two_word[1]
    
    def eliminate_user(self):
        k = max(0, len(self.context.map_user) - self.game.size_user_pool)
        list_uid = list(self.context.map_user.keys())
        list_eliminate_uid = random.sample(list_uid, k)
        for uid in list_eliminate_uid:
            self.context.map_user.pop(uid)