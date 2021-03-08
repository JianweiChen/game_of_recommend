# coding=utf8

from run_step import RunStep

class RunStepRestoreContext(RunStep):
    
    def __init__(self, hyper_param):
        super().__init__(hyper_param)
    
    def real_run(self, context):
        return context