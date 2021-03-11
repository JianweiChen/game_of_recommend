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

class StepRecommend(Step):

    def __init__(self, game, need_summary=False):
        super().__init__(game, need_summary)
    
    # Divided into four experimental groups, 
    #   A: all random, 
    #   B: model for recall, 
    #   C: model for recall and CTR, 
    #   D: model for recall and CTR and PAY
    def real_run(self):
        ctx = self.context
        for uid, user in ctx.map_user.items():
            list_tid_rsp = self.sort(user)
            user.list_tid_recommend = []
            for tid in list_tid_rsp:
                user.list_tid_recommend.append(tid)

    # The `SORT` interface is the outermost interface of the recommendation system
    def sort(self, user):
        ab_version = self.game.example_manager.get_user_ab_version(user)
        list_tid_rsp = []
        # todo
        if ab_version == 'X':
            pass
        else:
            list_tid_rsp = self.sort_random(user)
        return list_tid_rsp

    # Random recommendation, but including dedup strategy, as a baseline
    def sort_random(self, user):
        game = self.game
        list_tid = self.dedup_to_list_id(user)
        k = min(game.count_item_per_recommend, len(list_tid))
        return random.sample(list_tid, k)

    # Do dedup and return items that can be recommended to this user
    def dedup_to_list_id(self, user):
        ctx = self.context
        return list(set(ctx.map_item.keys()) - set(user.map_impression.keys()))

