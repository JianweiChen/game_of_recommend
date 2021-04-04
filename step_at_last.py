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

# Statistics various indicators for a AB-group of users
class AbVersionStat(object):

    def __init__(self):
        self.click_neg = 0
        self.click_pos = 0
        self.pay_zero = 0
        self.pay = 0

    @property
    def ctr(self):
        if self.len_preclk <= 0:
            return -1.
        return self.click_pos / self.len_preclk

    @property
    def len_preclk(self):
        return self.click_pos + self.click_neg
    
    @property
    def pay_avg(self):
        if self.len_preclk <= 0:
            return -1.
        return self.pay / self.len_preclk

class StepAtLast(Step):

    def __init__(self, game, need_summary=False):
        super().__init__(game, need_summary)
    
    def real_run(self):
        self.stat_example()
        self.display_condition()

    def display_condition(self):
        map_summary = self.context.map_summary
        # list_message.append("Loop %s" % self.context.loop)
        # list_message.append("A_ctr\t%.3f\tB_ctr\t%.3f" % (
        #     map_summary['A_ctr'], map_summary['B_ctr']
        # ))
        # list_message.append("C_ctr\t%.3f\tD_ctr\t%.3f" % (
        #     map_summary['C_ctr'], map_summary['D_ctr']
        # ))
        list_message = [
            "loop=%s\tLoss=%.3f\t%.3f" % (self.context.loop, map_summary['loss'], map_summary['auc']),
        ]
        list_message.append()
        print("\n".join(list_message))

    def stat_example(self):
        summary = self.context.map_summary
        map_ab = dict()
        for ab_version in self.game.example_manager.list_ab_version:
            map_ab[ab_version] = AbVersionStat()
        
        list_example_click = self.example_manager.load_example_click(self.context.loop)
        for example_data in list_example_click:
            ab_version = example_data['ab_version']
            label = example_data['label']
            ab_stat = map_ab[ab_version]
            if label > 0:
                ab_stat.click_pos += 1
            else:
                ab_stat.click_neg += 1
        list_example_pay = self.example_manager.load_example_pay(self.context.loop)
        for example_data in list_example_pay:
            ab_version = example_data['ab_version']
            label = example_data['label']
            ab_stat = map_ab[ab_version]
            ab_stat.pay += label
        for ab_version, ab_stat in map_ab.items():
            summary['%s_ctr' % ab_version] = ab_stat.ctr
            summary['%s_preclk' % ab_version] = ab_stat.len_preclk
            summary['%s_pay' % ab_version] = ab_stat.pay