# coding=utf8

import os
import sys
import random
import logging
import pickle
import json

from run_step_bulid_corpus import RunStepBuildCorpus
from run_step_create_item import RunStepCreateItem
from run_step_create_user import RunStepCreateUser
from run_step_recommend import RunStepRecommend
from run_step_train import RunStepTrain
from run_step_summary import RunStepSummary
from run_step_build_ann import RunStepBuildAnn
from run_step_at_last import RunStepAtLast

from hyper_param import HyperParam
from game_context import GameContext
from fm_model import FmModel
from deep_fm_model import DeepFmModel

class GameEngine(object):
    def __init__(self, hyper_param, loop_count=100):
        self.hyper_param = hyper_param
        self.loop_count = loop_count
        self.init_log()
        self.topology = [
            RunStepBuildCorpus(self),
            RunStepCreateItem(self),
            RunStepCreateUser(self),
            RunStepRecommend(self),
            RunStepTrain(self),
            RunStepBuildAnn(self),
            RunStepSummary(self),
            RunStepAtLast(self),
        ]
        self.init_or_restore_context()
        self.init_or_restore_model()
        self.context.hyper_param = hyper_param
        self.init_or_clear_example_path()

        self.example_data_message_queue = []

    
    def init_or_clear_example_path(self):
        example_path = self.hyper_param.k_example_path
        if not os.path.exists(example_path):
            os.mkdir(example_path)
        if self.context.loop_count <= 1: # restore from dumped context
            for name in os.listdir(example_path):
                if name.endswith('.example.txt'):
                    os.remove(os.path.join(example_path, name))
    
    def init_or_restore_model(self):
        if True:
            self.model_map = dict(
                base_fm=FmModel(),
                deep_base_fm=DeepFmModel()
            )

    def init_log(self):
        logging.basicConfig(filename=self.hyper_param.k_log_path)
        if self.hyper_param.k_logging_debug_mode:
            logging.getLogger().setLevel(logging.DEBUG)
        else:
            logging.getLogger().setLevel(logging.INFO)
    
    def init_or_restore_context(self):
        if os.path.exists(self.hyper_param.k_context_dump_path):
            with open(self.hyper_param.k_context_dump_path, 'rb') as f:
                self.context = pickle.load(f)
                logging.info('restore context from dump-context')
        else:
            self.context = GameContext(self.hyper_param)
            logging.info("no dump-context found, use a new GameContext")
                

    def run(self):
        logging.info("game engine start")
        while self.context.loop_count < self.loop_count:
            self.context.loop_count += 1
            for run_step in self.topology:
                run_step.run()
        logging.info("game engine shut down for reaching the maximum number of loop")

if __name__ == '__main__':
    pass
