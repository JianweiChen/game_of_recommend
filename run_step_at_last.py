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

        # dump context
        if context.loop_count % hyper_param.k_context_dump_interval != 0:
            return context
        with open(hyper_param.k_context_dump_path, 'wb') as fw:
            pickle.dump(context, fw)
    