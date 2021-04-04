# coding=utf8
import random

from base import Base

# This module is used to determine the user's click and pay behavior
# In order to simulate the user's behavior, the positional relationship between 
# words is used here to generate the user's behavior. It makes sense to use the 
# NLP problem to simulate the user behavior of the recommendation system, because 
# they all have the characteristics of large-scale discrete features. The difference 
# is that some randomness is included in the recommendation scenario, and this module 
# also considers the randomness.
class JudgeManager(Base):
    
    def __init__(self, game):
        super().__init__(game)
    
    # Whether the item-word will appear between two user-words determines whether 
    # the user will click. When this two-clamp-one scenario appears, the closer the distance 
    # between the two user words, the greater the probability that the user will click
    def judge_click(self, user, item):
        ctx = self.context
        word_a = user.word_a
        word_b = user.word_b
        word_t = item.word_t
        if word_t in (word_a, word_b):
            return False
        # paragraph_a_set = set(ctx.map_word_paragraph.get(word_a, dict()).keys())
        # paragraph_b_set = set(ctx.map_word_paragraph.get(word_b, dict()).keys())
        # paragraph_t_set = set(ctx.map_word_paragraph.get(word_t, dict()).keys())
        # paragraph_set = paragraph_a_set & paragraph_b_set & paragraph_t_set
        paragraph_set = self.word_simultaneously([word_a, word_b, word_t])
        if not paragraph_set:
            return False
        list_paragraph = list(paragraph_set)
        random.shuffle(list_paragraph)
        k = int(len(list_paragraph) * self.game.rate_paragraph_ctr_search)
        list_paragraph = list_paragraph[:k]
        list_min_ab_distance = []
        for paragraph_id in list_paragraph:
            r = self.calc_min_ab_distance(paragraph_id, word_a, word_b, word_t)
            list_min_ab_distance.append(r)
        list_min_ab_distance = sorted(list_min_ab_distance, reverse=False)
        # print(user, list_min_ab_distance)
        for r in list_min_ab_distance:
            if random.random() < 1. / (max(1, r - self.game.bias_distance_click)):
                return True
            if random.random() < self.game.prob_dislike_click:
                return False
        return False
    
    # Similar to the click scenario, but the factor that determines the payment value 
    # is not the distance between two user words, but the distance between the item 
    # word and any user in a single time. The closer the distance, the higher the user may pay
    def judge_pay(self, user, item):
        ctx = self.context
        word_a = user.word_a
        word_b = user.word_b
        word_t = item.word_t
        if word_t in (word_a, word_b):
            return 0
        paragraph_set = self.word_simultaneously([word_a, word_b, word_t])
        if not paragraph_set:
            return 0
        list_paragraph = list(paragraph_set)
        random.shuffle(list_paragraph)
        k = int(len(list_paragraph) * self.game.rate_paragraph_ctr_search)
        list_paragraph = list_paragraph[:k]
        list_min_ta_or_tb_distance = []
        for paragraph_id in list_paragraph:
            r = self.calc_min_ta_or_tb_distance(paragraph_id, word_a, word_b, word_t)
            list_min_ta_or_tb_distance.append(r)
        list_min_ta_or_tb_distance = sorted(list_min_ta_or_tb_distance, reverse=False)
        pay = 0
        for r in list_min_ta_or_tb_distance:
            pay += max(0, self.game.bias_distance_pay - r)
        # todo: Use the number of common paragraphs as the denominator 
        # to avoid homogeneity with click behavior
        pay = self.game.scale_pay * pay / (1 + len(ctx.list_paragraph_id))
        # pay = int(pay)
        return pay

    # Return a collection of paragraphs where multiple words appear at the same time
    def word_simultaneously(self, list_word):
        assert len(list_word) >= 2
        list_paragraph_set = [
            set(self.context.map_word_paragraph.get(word, dict()).keys())
            for word in list_word
        ]
        result_set = list_paragraph_set[0]
        for i in range(1, len(list_paragraph_set)):
            result_set &= list_paragraph_set[i]
        return result_set
    
    # In the current paragraph, the nearest ab pair when the following conditions are met:
    #   1) a appears before b
    #   2) t appears between a and b
    #   3) a and b and t are not equal to each other
    # If the above-mentioned ab pair does not exist, then the total number of words in the 
    # paragraph is returned
    def calc_min_ab_distance(self, paragraph_id, word_a, word_b, word_t):
        m = self.context.map_word_paragraph
        list_a = m[word_a][paragraph_id]
        list_b = m[word_b][paragraph_id]
        list_t = m[word_t][paragraph_id]
        min_ab_distance = self.game.count_word_per_paragraph
        for b in list_b:
            for a in list_a:
                if a > b:
                    break
                for t in list_t:
                    if t > b:
                        break
                    if t > a:
                        min_ab_distance = min(min_ab_distance, b-a)
                        break
        return min_ab_distance
    
    # In the current paragraph, the nearest ta pair or tb pair when the following conditions are met:
    #   1) a appears before b
    #   2) t appears between a and b
    #   3) a and b and t are not equal to each other
    # If the above-mentioned ab pair does not exist, then the total number of words in the 
    # paragraph is returned
    def calc_min_ta_or_tb_distance(self, paragraph_id, word_a, word_b, word_t):
        m = self.context.map_word_paragraph
        list_a = m[word_a][paragraph_id]
        list_b = m[word_b][paragraph_id]
        list_t = m[word_t][paragraph_id]
        min_ta_or_tb_distance = self.game.count_word_per_paragraph
        for t in list_t:
            if list_b[-1] < t:
                break
            for a in list_a:
                if a > t:
                    break
                min_ta_or_tb_distance = min(min_ta_or_tb_distance, t-a)
        for t in list_t:
            if list_a[0] > t:
                break
            for b in list_b[::-1]:
                if b < t:
                    break
                min_ta_or_tb_distance = min(min_ta_or_tb_distance, b-t)
        return min_ta_or_tb_distance