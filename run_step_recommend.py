# coding=utf8
import random
from run_step import RunStep

class RunStepRecommend(RunStep):

    def __init__(self, game_engine):
        super().__init__(game_engine)
    
    def real_run(self):
        context = self.context
        hyper_param = self.hyper_param
        for uid in context.user_map:
            user = context.user_map[uid]
            ab_version = self.get_ab_version(user)
            # Retrieval
            retrieval_tid_list = self.retrieve(user)
            input_item_list = [
                context.item_map[tid] for tid in retrieval_tid_list
                if not context.is_dup(uid, tid)]
            # Rank
            ranked_item_list = self.rank(user, input_item_list)
            n = hyper_param.k_impression_count_per_req
            impression_item_list = ranked_item_list[:n]
            # User Action
            self.user_action_to_emit_example(user, impression_item_list)
        return context
    
    def retrieve(self, user):
        # todo, use double tower ann to retrieve
        context = self.context
        hyper_param = self.hyper_param
        tid_list = list(context.item_map.keys())
        return random.sample(tid_list, hyper_param.k_rank_input_item_count)
    
    def rank(self, user, input_item_list):
        # todo, use model
        ranked_item_list = input_item_list
        return ranked_item_list
    
    def user_action_to_emit_example(self, user, impression_item_list):
        game_engine = self.game_engine
        for item in impression_item_list:
            click = self.judge_click(user, item)
            label = 0.
            if click:
                label = 1.
            example_data = dict(
                f_uid=user.uid,
                f_tid=item.tid,
                label=label,
                m_user="%s_%.2f%%" % (user, 100.*user.prior_ctr),
                m_item=str(item),
            )
            game_engine.example_data_message_queue.append(example_data)
            


    def get_ab_version(self, user):
        uid = user.uid
        if (uid//23) % 2 == 0:
            return 'A'
        else:
            return 'B'
    