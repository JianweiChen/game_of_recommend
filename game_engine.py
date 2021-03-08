# coding=utf8

import os
import sys
import random
import logging

from run_step_bulid_corpus import RunStepBuildCorpus
from run_step_create_item import RunStepCreateItem
from run_step_create_user import RunStepCreateUser
from run_step_restore_context import RunStepRestoreContext
from run_step_recommend import RunStepRecommend
from run_step_train import RunStepTrain
from run_step_summary import RunStepSummary
from run_step_dump_context import RunStepDumpContext

from hyper_param import HyperParam
from game_context import GameContext

class GameEngine(object):
    def __init__(self, hyper_param):
        self.hyper_param = hyper_param
        self.init_log()
        self.topology = [
            RunStepRestoreContext(hyper_param),
            RunStepBuildCorpus(hyper_param),
            RunStepCreateItem(hyper_param),
            RunStepCreateUser(hyper_param),
            RunStepRecommend(hyper_param),
            RunStepTrain(hyper_param),
            RunStepDumpContext(hyper_param),
            RunStepSummary(hyper_param),
        ]
        self.context = GameContext(hyper_param)

        self.context_restored = False
    
    def init_log(self):
        logging.basicConfig(filename=self.hyper_param.k_log_path)
        if self.hyper_param.k_logging_debug_mode:
            logging.getLogger().setLevel(logging.DEBUG)
        else:
            logging.getLogger().setLevel(logging.INFO)

    def run(self):
        logging.info("game engine start")
        while self.context.loop_count < self.hyper_param.k_loop_count:
            self.context.loop_count += 1
            for run_step in self.topology:
                self.context = run_step.run(self.context)

if __name__ == '__main__':
    pass
