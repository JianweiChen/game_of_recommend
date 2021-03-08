# coding=utf8
import logging
from run_step import RunStep

class RunStepSummary(RunStep):

    def __init__(self, hyper_param):
        super().__init__(hyper_param)
    
    def real_run(self, context):
        summary_list = [
            "paragraph count is %s" % len(context.paragraph_id_queue),
            # "first 5 in paragraph queue are %s" % context.paragraph_id_queue[:5],
            # "last 5 in paragraph queue are %s" % context.paragraph_id_queue[-5:],
            "word count is %s" % len(context.word_paragraph_position_map),
            # "rank_word_list top 5 is %s" % (context.rank_word_list[:5]),
            # #  "built_corpus_name_set is %s" % context.built_corpus_name_set),
            "built_corpus_name_set size is %s" % len(context.built_corpus_name_set),
            "buffer_word_list size is %s" % len(context.buffer_word_list),
            "get two word random: %s" % (context.get_random_word(2))
        ]
        # print('\n'.join(summary_list))
        for summary_message in summary_list:
            context.debug(summary_message, self)
        return context