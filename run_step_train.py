# coding=utf8
import logging
from run_step import RunStep

class RunStepTrain(RunStep):

    def __init__(self, hyper_param):
        super().__init__(hyper_param)
    
    def real_run(self, context):
        return context
    