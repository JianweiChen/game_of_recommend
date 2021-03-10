# coding=utf8

import os
import sys
import json
import pickle
import random
import string
import math
import time

from step import Step

class StepANN(Step):

    def __init__(self, game, need_summary=False):
        super().__init__(game, need_summary)
    
    def real_run(self):
        pass