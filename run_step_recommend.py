# coding=utf8
import random
from run_step import RunStep
import tensorflow as tf

class RunStepRecommend(RunStep):

    def __init__(self, game_engine):
        super().__init__(game_engine)
    
    def real_run(self):
        context = self.context
        hyper_param = self.hyper_param
        for uid in context.user_map:
            user = context.user_map[uid]
            ab_version = self.game_engine.get_ab_version(user)
            # Retrieval
            retrieval_tid_list = self.retrieve(user)
            input_item_list = [
                context.item_map[tid] for tid in retrieval_tid_list
                if not context.is_dup(uid, tid)]
            # Rank
            ranked_item_list = self.rank(user, input_item_list, ab_version)
            n = hyper_param.k_impression_count_per_req
            impression_item_list = ranked_item_list[:n]
            # User Action
            self.user_action_to_emit_example(user, impression_item_list)
        # stat ctr
        q = self.game_engine.example_manager.preclk_example_message_queue
        r = dict(
            A=dict(neg=0,pos=0),
            B=dict(neg=0,pos=0)
        )
        for d in q:
            user = self.context.user_map[int(d['f_uid'])]
            ab_version = self.game_engine.get_ab_version(user)
            pos_or_neg = 'pos' if d['label'] > 0 else 'neg'
            r[ab_version][pos_or_neg] += 1
        a_ctr = r['A']['pos'] / (r['A']['pos'] + r['A']['neg'])
        b_ctr = r['B']['pos'] / (r['B']['pos'] + r['B']['neg'])
        context.info("a_ctr=%s, b_ctr=%s" % (a_ctr, b_ctr), self)
        # dump example 
        self.game_engine.example_manager.dump_example_in_queue(self.context.loop_count)
    
    def retrieve(self, user):
        # todo, use double tower ann to retrieve
        context = self.context
        hyper_param = self.hyper_param
        tid_list = list(context.item_map.keys())
        if hyper_param.k_rank_input_item_count >= len(tid_list):
            return tid_list
        else:
            return random.sample(tid_list, hyper_param.k_rank_input_item_count)
    
    def rank(self, user, input_item_list, ab_version='A'):
        if ab_version == 'A':
            score_list = self.calc_pred(user, input_item_list)
            item_score_list = zip(input_item_list, score_list)
            item_score_list = sorted(item_score_list, key=lambda x: x[1], reverse=True)
            # print(user, item_score_list[0], item_score_list[-1])
            ranked_item_list = [
                x[0] for x in item_score_list
            ]
        else:
            ranked_item_list = input_item_list
            random.shuffle(ranked_item_list)
        return ranked_item_list
    
    def user_action_to_emit_example(self, user, impression_item_list):
        game_engine = self.game_engine
        for item in impression_item_list:
            self.context.dedup_set.add('%s_%s' % (user.uid, item.tid))
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
            game_engine.example_manager.emit_preclk_example(example_data)

    def calc_pred(self, user, item_list):
        ctr_model = self.model_map['base_fm']
        d = dict(
            f_uid=[],
            f_tid=[]
        )
        labels = []
        for item in item_list:
            d['f_uid'].append(str(user.uid))
            d['f_tid'].append(str(item.tid))
            labels.append(0.)
        ds = tf.data.Dataset.from_tensor_slices((d, labels))
        ds = ds.batch(32)
        # print(ds.take(1).as_numpy_iterator().next())
        pred_score_list = ctr_model.predict(ds)
        return [
            pred[0] for pred in pred_score_list
        ]
