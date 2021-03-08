

class HyperParam(object):
    def __init__(self):
        self.k_logging_debug_mode = True
        # self.k_logging_debug_mode = False

        self.k_context_restore_path = None

        self.k_log_path = "/tmp/game_engine.log"

        self.k_loop_count = 10

        self.k_paragraph_word_count = 300

        self.k_user_pool_size = 1_000
        self.k_item_pool_size = 10_000

        self.k_paragraph_pool_size = 10_000
        self.k_new_paragraph_count_per_loop = 200

        self.k_item_word_rank_p = 0.3
        self.k_user_word_rank_p = 0.1

        # a big `k_ab_distance_bias` bring big prior ctr
        self.k_ab_distance_bias = 30
        self.k_user_click_prob_scale = 0.9
        self.k_user_dislike_prob = 0.01

        self.k_ab_distance_sample_prob = 1.

        self.k_create_user_count_per_loop = 1_000

        self.k_corpus_dir_path = '/Users/jianweichen/Desktop/game_of_recommend_corpus'

