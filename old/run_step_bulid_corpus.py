# coding=utf8
import os
import random
import string
import logging
import re

from run_step import RunStep
from hyper_param import HyperParam

class BuildCorpusError(Exception):
    pass

class RunStepBuildCorpus(RunStep):
    
    def __init__(self, game_engine):
        super().__init__(game_engine)
    
    def real_run(self):
        context = self.context
        c1 = self.hyper_param.k_paragraph_word_count
        c2 = self.hyper_param.k_new_paragraph_count_per_loop
        c3 = self.hyper_param.k_paragraph_pool_size
        word_count_need = c1 * c2
        word_count_need -= len(context.buffer_word_list)
        if word_count_need > 0:
            self.parse_to_buffer_word_list(context, word_count_need)
        for i in range(c2):
            paragraph_word_list = context.buffer_word_list[i*c1: (i+1)*c1]
            self.build_paragraph(context, paragraph_word_list)
        context.buffer_word_list = context.buffer_word_list[(i+1)*c1:]
        q = context.paragraph_id_queue
        paragraph_id_list_to_remove = []
        while len(q) > c3:
            paragraph_id_list_to_remove.append(q.pop(0))
        self.remove_paragraph(context, paragraph_id_list_to_remove)
        self.sort_word_list_by_paragraph_count(context)
        return context
    
    def parse_to_buffer_word_list(self, context, word_count_need):
        name_set = set(os.listdir(self.hyper_param.k_corpus_dir_path))
        name_set -= context.built_corpus_name_set
        name_list = list(name_set)
        for name in name_list:
            path = os.path.join(self.hyper_param.k_corpus_dir_path, name)
            with open(path, 'r') as f:
                s = ' '.join(list(f.readlines()))
            s = self._format_string(s)
            word_list = s.split(' ')
            context.buffer_word_list.extend(word_list)
            word_count_need -= len(word_list)
            logging.debug("%s built with word_count_need is %s" % (name, word_count_need))
            context.built_corpus_name_set.add(name)
            if word_count_need <= 0:
                break
        if word_count_need > 0:
            raise BuildCorpusError('Corpus exhaustion!!!')
    
    def build_paragraph(self, context, word_list):
        assert len(word_list) == self.hyper_param.k_paragraph_word_count
        q = context.paragraph_id_queue
        paragraph_id = q[-1] + 1 if len(q) else 1
        m = context.word_paragraph_position_map
        for position, word in enumerate(word_list):
            if word not in m:
                m[word] = dict()
            if paragraph_id not in m[word]:
                m[word][paragraph_id] = list()
            m[word][paragraph_id].append(position)
        q.append(paragraph_id)
    
    def remove_paragraph(self, context, paragraph_id_list):
        if not paragraph_id_list:
            return
        m = context.word_paragraph_position_map
        for word in m:
            for paragraph_id in paragraph_id_list:
                if paragraph_id in m[word]:
                    m[word].pop(paragraph_id)
    
    def sort_word_list_by_paragraph_count(self, context):
        context.rank_word_list = [
            pair[0] for pair in 
            sorted(context.word_paragraph_position_map.items(), 
                key=lambda pair: len(pair[1]), reverse=True)
        ]

    def _format_string(self, s):
        s = s.lower()
        s = re.sub(r'</?\w+[^>]*>', ' ', s)
        s = re.sub('[^%s]' % re.escape(string.ascii_lowercase), ' ', s)
        # s = re.sub('[%s]' % re.escape(string.digits), '', s)
        # s = re.sub('[%s]' % re.escape(string.punctuation), ' ', s)
        s = re.sub('[%s]+' % re.escape(string.whitespace), ' ', s)
        s = s.strip()
        return s



        
if __name__ == '__main__':
    rs = RunStepBuildCorpus(hyper_param=HyperParam())
    s = rs._format_string("我•ª˙ªøa ,10big <p> </p>girl")
    print(s)