# coding=utf8

from base import Base

class JudgeManager(Base):
    
    def __init__(self, game):
        super().__init__(game)
    
    def judge_click(self, user, item):
        _ctx = self.context
        word_a = user.word_a
        word_b = user.word_b
        word_t = item.word_t
        
        return False
    
    def judge_pay(self, user, item):
        return False
    
    def calc_min_ab_distance(self, paragraph_id, word_a, word_b, word_t):
        return 2
    
    def calc_min_ta_or_tb_distance(self, paragraph_id, word_a, word_b, word_t):
        return 1