# coding=utf8

import logging

class Context(object):
    
    def __init__(self):
        
        self.loop = 0
        self.map_word_paragraph = dict()
        self.map_user = dict()
        self.map_item = dict()
        self.map_corpus = dict()
        self.list_paragraph_id = []
        self.list_buffer_word = []
        self.list_rank_word = []

        self.map_summary = dict()

    def summary(self, caller):
        list_message = []
        for k, v in self.__dict__.items():
            if isinstance(v, dict) or isinstance(v, list):
                list_message.append(
                    "len(%s)=%s" % (k, len(v))
                )
            if isinstance(v, int) or isinstance(v, float):
                list_message.append(
                    "%s=%s" % (k, v)
                )
        for k, v in self.map_summary.items():
            list_message.append(
                "%s=%s" % (k, v)
            )
        list_message.append("caller=%s" % caller.__class__)
        message = ' '.join(list_message)
        logging.info(message)