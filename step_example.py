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

class StepExample(Step):

    def __init__(self, game, need_summary=False):
        super().__init__(game, need_summary)
    
    def real_run(self):
        judge = self.game.judge_manager
        # pos, neg = 0, 0
        for uid, user in self.context.map_user.items():
            for tid in user.list_tid_recommend:
                item = self.context.map_item[tid]
                user.map_impression[item.tid] = True
                # judge click and emit click example
                click = judge.judge_click(user, item)
                self.emit_example(user, item, example_type='click', example_label=1. if click else 0.)
                if click:
                    # if user clicks, judge pay value and emit pay example
                    pay = judge.judge_pay(user, item)
                    self.emit_example(user, item, example_type='pay', example_label=pay)
        # print("ctr=%s" % (pos/(pos+neg)))
        self.game.example_manager.dump()

    def emit_example(self, user, item, example_type, example_label):
        assert example_type in ('click', 'pay')
        example_manager = self.game.example_manager
        example_data = dict(
            f_uid=user.uid,
            f_tid=item.tid,
            s_user=str(user),
            s_item=str(item),
            label_type=example_type,
            label=example_label,
            ab_version=example_manager.get_user_ab_version(user)
        )
        if example_type == 'click':
            example_manager.emit_click(example_data)
        elif example_type == 'pay':
            example_manager.emit_pay(example_data)