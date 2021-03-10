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

    def __init__(self, game):
        super().__init__(game)
    
    # Divided into four experimental groups, 
    #   A: all random, 
    #   B: model for recall, 
    #   C: model for recall and CTR, 
    #   D: model for recall and CTR and PAY
    def real_run(self):
        ctx = self.context
        for uid, user in ctx.map_user.items():
            user.list_tid_impression = []
            for tid in list_tid_rsp:
                user.list_tid_impression.append(tid)
    
    def sort(self, user):
        list_tid_rsp = []

        return list_tid_rsp