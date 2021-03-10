# coding=utf8
import random
from run_step import RunStep
from user import User

class RunStepCreateUser(RunStep):
    
    def __init__(self, game_engine):
        super().__init__(game_engine)
    
    def real_run(self):
        context = self.context
        context.info('RunStepCreateUser start', self)
        new_user_count = 0
        user_pool_is_full = False
        for _ in range(self.hyper_param.k_create_user_count_per_loop):
            two_word = context.get_random_word(2, self.hyper_param.k_user_word_rank_p)
            user = User(two_word[0], two_word[1])
            if user.uid not in context.user_map and self.is_qualified_user(user):
                # context.debug("good user %s_%.2fs%%" % (user, 100.*user.prior_ctr))
                context.user_map[user.uid] = user
                new_user_count += 1
                user_pool_is_full = len(context.user_map) >= self.hyper_param.k_user_pool_size
                if user_pool_is_full and new_user_count >= self.hyper_param.k_user_eliminate_max:
                    break
        # eliminate randomly
        if user_pool_is_full:
            user_count_to_eliminate = len(context.user_map) - self.hyper_param.k_user_pool_size
            uid_list_to_eliminate = random.sample(list(context.user_map.keys()), user_count_to_eliminate)
            for uid in uid_list_to_eliminate:
                context.user_map.pop(uid)
        return context

    def is_qualified_user(self, user):
        context = self.context
        if user.word_a == user.word_b:
            return False
        pos, neg = 0, 0
        for tid in context.item_map:
            item = context.item_map[tid]
            if self.judge_click(user, item):
                pos += 1
            else:
                neg += 1
        ctr = pos / (pos+neg)
        user.set_prior_ctr(ctr)
        if ctr > self.hyper_param.k_user_qualified_ctr:
            return True
        else:
            return False
        return True

        
