# coding=utf8

from base import Base

class Step(Base):

    def __init__(self, game, need_summary=False):
        super().__init__(game)
        self.need_summary = need_summary

    def run(self):
        self.real_run()
        if self.need_summary:
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