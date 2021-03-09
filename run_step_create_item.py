# coding=utf8
import logging
import random
from run_step import RunStep
from item import Item

class RunStepCreateItem(RunStep):
    
    def __init__(self, game_engine):
        super().__init__(game_engine)
    
    def real_run(self):
        hyper_param = self.hyper_param
        context = self.context
        p = self.hyper_param.k_item_word_rank_p
        k = int(len(context.rank_word_list) * p)
        word_list_to_create_item = list(
            set(context.rank_word_list[:k]) - context.item_word_set
        )
        list_add_max = max(
            hyper_param.k_item_pool_size - len(context.item_map),
            hyper_param.k_item_eliminate_max
        )
        random.shuffle(word_list_to_create_item)
        word_list_to_create_item = word_list_to_create_item[:list_add_max]
        for word_t in word_list_to_create_item:
            item = Item(word_t)
            context.item_map[item.tid] = item
            context.item_word_set.add(word_t)
        context.debug("word_list_to_create_item size is %s" % len(word_list_to_create_item), self)
        context.debug("item_map size is %s" % len(context.item_map), self)
        return context