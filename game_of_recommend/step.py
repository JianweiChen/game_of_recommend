# coding=utf8

from base import Base

class Step(Base):

    def __init__(self, game):
        super().__init__(game)

    def run(self):
        self.real_run()
        self.context.summary(self)
    
    def real_run(self):
        raise NotImplementedError

    @property
    def example_manager(self):
        return self.game.example_manager
    
    @property
    def model_manager(self):
        return self.game.model_manager
    
    @property
    def judge_manager(self):
        return self.game.judge_manager