# coding=utf8
import os
import sys
import logging
import json
import pickle
from run_step import RunStep

class RunStepAtLast(RunStep):

    def __init__(self, game_engine):
        super().__init__(game_engine)
    
    def real_run(self):
        context = self.context
        hyper_param = self.hyper_param
        game_engine = self.game_engine
        
        # statistic ctr
        q = game_engine.example_data_message_queue
        pos, neg = 0, 0
        for d in q:
            if d['label'] > 0:
                pos += 1
            else:
                neg += 1
        ctr_stat = pos / (pos+neg)
        context.info("ctr=%s, example_count=%s" % (ctr_stat, pos+neg), self)                

        # dump train example
        path = context.get_preclk_example_path()
        q = game_engine.example_data_message_queue
        with open(path, 'w') as fw:
            while len(q) > 0:
                data = q.pop(0)
                line = json.dumps(data)
                fw.write("%s\n" % line)

        # dump context
        if context.loop_count % hyper_param.k_context_dump_interval != 0:
            return context
        with open(hyper_param.k_context_dump_path, 'wb') as fw:
            pickle.dump(context, fw)
    