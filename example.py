# coding=utf8
import os
import sys
import json
import random
from base import Base

class ExampleManager(Base):
    
    def __init__(self, game):
        super().__init__(game)
        self.init_dir()

        self.list_ab_version = ['A', 'B', 'C', 'D']

        self.queue_example_click = []
        self.queue_example_pay = []
    
    def init_dir(self):
        if not os.path.exists(self.game.path_example_dir):
            os.mkdir(game.path_example_dir)
    
    def remove(self):
        game = self.game
        for name in os.listdir(game.path_example_dir):
            if name.endswith('.example.txt'):
                os.remove(os.path.join(game.path_example_dir, name))
    
    def dump(self):
        loop = self.context.loop
        path_click = os.path.join(self.game.path_example_dir, 'example_click_%04d.example.txt' % loop)
        with open(path_click, 'w') as fw:
            while len(self.queue_example_click):
                example = self.queue_example_click.pop(0)
                line = json.dumps(example) + "\n"
                fw.write(line)
        path_pay = os.path.join(self.game.path_example_dir, 'example_pay_%04d.example.txt' % loop)
        with open(path_pay, 'w') as fw:
            while len(self.queue_example_pay):
                example = self.queue_example_pay.pop(0)
                line = json.dumps(example) + "\n"
                fw.write(line)
    
    def load_example_click(self, loop):
        return self._load_example(loop, 'click')
    
    def load_example_pay(self, loop):
        return self._load_example(loop, 'pay')

    def _load_example(self, loop, example_type):
        assert example_type in ('click', 'pay')
        path = os.path.join(self.game.path_example_dir, 'example_%s_%04d.example.txt' %(
            example_type, loop
        ))
        with open(path, 'r') as f:
            lines = list(f)
            list_example = [
                json.loads(line.strip()) for line in lines
            ]
            return list_example
    
    def emit_click(self, example):
        self.queue_example_click.append(example)
    
    def emit_pay(self, example):
        self.queue_example_pay.append(example)
    
    def get_user_ab_version(self, user):
        uid = user.uid
        size_ab_version = len(self.list_ab_version)
        ab_version_idx = (uid // 23) % size_ab_version
        ab_version = self.list_ab_version[ab_version_idx]
        return ab_version