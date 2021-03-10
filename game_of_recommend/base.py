# coding=utf8

class Base(object):

    def __init__(self, game):
        self.game = game
    
    @property
    def context(self):
        return self.game.context