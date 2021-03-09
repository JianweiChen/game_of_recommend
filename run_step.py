# coding=utf8
import os
import sys
import random
import logging
class RunStep(object):
    def __init__(self, game_engine):
        super().__init__()
        self.game_engine = game_engine

    @property
    def context(self):
        return self.game_engine.context
    
    @property
    def hyper_param(self):
        return self.game_engine.hyper_param
    
    @property
    def model_map(self):
        return self.game_engine.model_map

    def run(self):
        # logging.info("run loop=%s %s" % (context.loop_count, self.__class__))
        return self.real_run()
    #todo remove input param: context
    def real_run(self):
        raise NotImplementedError
    
    def judge_click(self, user, item):
        context = self.context
        if item.word_t in (user.word_a, user.word_b):
            return False
        m = context.word_paragraph_position_map
        a_set = set(m[user.word_a])
        b_set = set(m[user.word_b])
        t_set = set(m[item.word_t])
        abt_list = list(a_set & b_set & t_set)
        if self.hyper_param.k_ab_distance_sample_prob < 0.9999:
            k = int(self.hyper_param.k_ab_distance_sample_prob * len(abt_list))
            random.shuffle(abt_list)
            abt_list = abt_list[:k]
        ab_distance_list = []
        for paragraph_id in abt_list:
            ab_distance_list.append(self.get_min_ab_distance(
                context, paragraph_id, user.word_a, user.word_b, item.word_t
            ))
        ab_distance_list = sorted(ab_distance_list)
        for ab_distance in ab_distance_list:
            p = 1. / (max(1, ab_distance - self.hyper_param.k_ab_distance_bias))
            p *= self.hyper_param.k_user_click_prob_scale
            if random.random() < p:
                return True
            if random.random() < self.hyper_param.k_user_dislike_prob:
                return False
        return False
    
    def get_min_ab_distance(self, context, paragraph_id, word_a, word_b, word_t):
        m = context.word_paragraph_position_map
        a_list = m[word_a][paragraph_id]
        b_list = m[word_b][paragraph_id]
        t_list = m[word_t][paragraph_id]
        min_ab_distance = self.hyper_param.k_paragraph_word_count
        for a in a_list:
            for b in b_list:
                if a > b:
                    continue
                for t in t_list:
                    if t > b:
                        continue
                    if t > a:
                        min_ab_distance = min(min_ab_distance, b-a)
                        break
        return min_ab_distance