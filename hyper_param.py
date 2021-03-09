

class HyperParam(object):
    def __init__(self):
        self.k_logging_debug_mode = True
        # self.k_logging_debug_mode = False

        self.k_context_restore_path = None

        # how many words one paragraph contains
        self.k_paragraph_word_count = 300

        self.k_user_pool_size = 1_000
        self.k_item_pool_size = 10_000

        # max count of user which will be eliminated from `user_map` every loop
        self.k_user_eliminate_max = 20
        # if 0, no need to eliminate item from `item_map`
        self.k_item_eliminate_max = 0

        self.k_paragraph_pool_size = 1000
        # how many paragraph will generate per loop, if paragraph pool is full
        #   then elimination will happen.
        self.k_new_paragraph_count_per_loop = 200
        # top words will used to generate item, ranked by paragraph count
        self.k_item_word_rank_p = 0.3
        # top words will used to generate user, ranked by paragraph count
        self.k_user_word_rank_p = 0.1
        # bigger `k_ab_distance_bias` brings bigger prior ctr
        self.k_ab_distance_bias = 3
        # max prob from biggist click motivation (with distance-bias)
        self.k_user_click_prob_scale = 0.9
        # probility of `return False` for one paragraph in `judge_click`
        self.k_user_dislike_prob = 0.01
        # bigger `k_user_qualified_ctr` brings harder qualified user creation
        self.k_user_qualified_ctr = 0.005

        self.k_ab_distance_sample_prob = 1.

        # how many items can be input of deep-fm rank module
        self.k_rank_input_item_count = 300

        self.k_impression_count_per_req = 1

        self.k_create_user_count_per_loop = 1_000
        self.k_context_dump_interval = 1
        self.k_corpus_dir_path = '/Users/jianweichen/Desktop/game_of_recommend_corpus'
        self.k_context_dump_path = '/Users/jianweichen/Desktop/game_of_recommend_context.pkl'
        self.k_log_path = "/tmp/game_engine.log"
        self.k_example_path = '/Users/jianweichen/Desktop/game_of_recommend_example'

