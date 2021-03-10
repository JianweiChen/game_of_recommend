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
        list_tid_rsp = []

        return list_tid_rsp