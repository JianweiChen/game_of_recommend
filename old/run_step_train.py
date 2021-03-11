# coding=utf8
import logging
from run_step import RunStep

class RunStepTrain(RunStep):

    def __init__(self, game_engine):
        super().__init__(game_engine)
    
    def real_run(self):
        ds = self.game_engine.example_manager.example_to_dataset(self.context.loop_count)
        history = self.game_engine.model_map['base_fm'].fit(ds, epochs=1)
        self.game_engine.model_map['base_fm'].evaluate(ds)
        auc = history.history['auc']
        loss = history.history['loss']
        self.context.info("loss=%s auc=%s" % (loss, auc), self)
        self.game_engine.model_map['base_fm'].fit(ds, epochs=self.hyper_param.k_train_epochs)