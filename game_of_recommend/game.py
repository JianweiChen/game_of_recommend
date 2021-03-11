# coding=utf8
import os
import pickle
import logging

from context import Context

from step_corpus import StepCorpus
from step_item import StepItem
from step_user import StepUser
from step_recommend import StepRecommend
from step_example import StepExample
from step_train import StepTrain
from step_ann import StepANN
from step_at_last import StepAtLast

from example import ExampleManager
from ml import ModelManager
from judge import JudgeManager

class Game(object):

    """Usage:
    >> game = Game(loop=100)
    >> game.run()
    """

    def __init__(self, loop):

        # Total number of rounds to run
        self.loop = loop

        ############
        # Hyper-parameter: The pool size and update intensity of corpus, user, and item
        ############
        self.size_user_pool = 20_000
        self.size_item_pool = 5_000
        self.size_paragraph_pool = 5_000
        self.size_new_item = 20
        self.size_new_user = 20
        self.size_solicit_attemp = 20_000
        self.size_new_paragraph = 20
        self.count_word_per_paragraph = 300

        ############
        # Hyper-parameters used to generate item and user
        ############
        self.rate_word_item = 0.5
        self.rate_word_user = 0.1

        ############
        # Hyper-parameters used to Determining the user's click 
        # and pay behavior based on the position of the word
        ############
        self.prob_dislike_click = 0.01
        self.rate_solicit_browse = 0.01
        self.bias_distance_click = 3
        self.bias_distance_pay = 300
        self.rate_paragraph_ctr_search = 1.
        self.rate_paragraph_pay_search = 1.
        self.scale_pay = 10_000

        ############
        # Hyper-params for recommendation
        ############
        self.count_item_per_recommend = 5
        self.count_input_fine_rank = 300

        # Model train
        self.model_click_adam_learning_rate = 0.01
        self.model_click_batch_size = 32
        self.model_click_extra_train_epochs = 2

        ############
        # Path on disk
        ############
        self.path_corpus_dir = "/Users/jianweichen/Desktop/game_of_recommend_corpus"
        self.path_example_dir = "/Users/jianweichen/Desktop/game_of_recommend_example"
        self.path_pkl = "/Users/jianweichen/Desktop/game_of_recommend.pkl"
        self.path_log_file = "/tmp/game_of_recommend.log"
        self.path_user_pkl = "/Users/jianweichen/Desktop/map_user_game_of_recommend.pkl"
        
        # Config of logging.
        logging.basicConfig(filename=self.path_log_file)
        logging.getLogger().setLevel(logging.INFO)

        # Manager modules that perform their duties
        self.example_manager = ExampleManager(self)
        self.model_manager = ModelManager(self)
        self.judge_manager = JudgeManager(self)

        # Try to load the context from the pickle file, similar to the 
        # checkpoint function, if it fails, initialize a new game environment
        if not self.load_context():
            self.init_new_game()
        
        # The main calculation steps
        self.build_steps()
    
    # Initialize a new game environment (Failed to load context)
    def init_new_game(self):
        self.context = Context()
        self.example_manager.remove()
        self.model_manager.remove()
        
    # Load a context checkpoint in `.pkl` format on disk
    def load_context(self):
        # todo
        return False

    def build_steps(self):
        self.steps = [
            # Load corpus or introduce new corpus to simulate the interest transfer of the group
            StepCorpus(self),
            # Use more frequent words to generate recommendation objects that are collectively referred to as items
            StepItem(self),
            # Use two more frequent words to generate a user (to be solicited here), the user will quickly 
            # browse a part of the item and decide whether the solicitation is successful
            StepUser(self),
            # Recommend, including dedup, retrieval, rank model for CTR and PAY
            StepRecommend(self),
            # The user consumes the recommended results and generates training samples called `Example`
            StepExample(self),
            # Training Model (FM, Deep-FM), and dump it
            StepTrain(self),
            # Recall of the 2-tower structure
            StepANN(self),
            # eg. To save the checkpoin of the context, etc.
            StepAtLast(self, need_summary=True),
        ]

    def run(self):
        while True:
            self.context.loop += 1
            self.run_one_loop()
            if self.context.loop >= self.loop:
                break
    # Run a round
    def run_one_loop(self):
        for step in self.steps:
            step.run()
        self.context.map_summary.clear()