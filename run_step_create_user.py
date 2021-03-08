# coding=utf8

from run_step import RunStep
from user import User

class RunStepCreateUser(RunStep):
    
    def __init__(self, hyper_param):
        super().__init__(hyper_param)
    
    def real_run(self, context):
        for _ in range(self.hyper_param.k_create_user_count_per_loop):
            two_word = context.get_random_word(2, self.hyper_param.k_user_word_rank_p)
            user = User(two_word[0], two_word[1])
            if user.uid not in context.user_map and self.is_qualified_user(context, user):
                # context.debug("good user %s_%.2fs%%" % (user, 100.*user.prior_ctr))
                context.user_map[user.uid] = user
        context.info("user_map size is %s" % (len(context.user_map)), self)
        return context

    def is_qualified_user(self, context, user):
        if user.word_a == user.word_b:
            return False
        pos, neg = 0, 0
        for tid in context.item_map:
            item = context.item_map[tid]
            if self.judge_click(context, user, item):
                pos += 1
            else:
                neg += 1
        ctr = pos / (pos+neg)
        user.set_prior_ctr(ctr)
        if ctr > 0.01:
            return True
        else:
            return False
        return True

        
