# coding=utf8
import logging
from run_step import RunStep
from item import Item

class RunStepCreateItem(RunStep):
    
    def __init__(self, hyper_param):
        super().__init__(hyper_param)
    
    def real_run(self, context):
        p = self.hyper_param.k_item_word_rank_p
        k = int(len(context.rank_word_list) * p)
        word_list_to_create_item = list(
            set(context.rank_word_list[:k]) - context.item_word_set
        )
        for word_t in word_list_to_create_item:
            item = Item(word_t)
            context.item_map[item.tid] = item
            context.item_word_set.add(word_t)
        context.debug("word_list_to_create_item size is %s" % len(word_list_to_create_item), self)
        context.debug("item_map size is %s" % len(context.item_map), self)
        return context