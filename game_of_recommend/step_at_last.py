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

class StepAtLast(Step):

    def __init__(self, game):
        super().__init__(game)
    
    def real_run(self):
        pass