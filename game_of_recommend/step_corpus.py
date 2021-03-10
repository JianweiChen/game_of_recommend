# coding=utf8

import os
import sys
import json
import pickle
import random
import string
import math
import time
import re

from step import Step

class StepCorpus(Step):

    def __init__(self, game):
        super().__init__(game)
        # Load the pathnames of all available corpus in advance, and then 
        # parse the content of the article as needed
        self.list_corpus_path = []
        for name in os.listdir(self.game.path_corpus_dir):
            path = os.path.join(self.game.path_corpus_dir, name)
            self.list_corpus_path.append(path)
    
    def real_run(self):
        ctx = self.context
        game = self.game
        self.new_some_paragraph()
        while not self.paragraph_pool_is_full:
            self.new_some_paragraph()
        self.remove_paragraph()
        self.rank_word()

    # When the paragraphs generated later make the paragraph pool too large, 
    # the earlier generated paragraphs will be eliminated first. Similar to the 
    # operation of a pipeline
    def remove_paragraph(self):
        m = self.context.map_word_paragraph
        list_word_empty = []
        while self.paragraph_pool_need_eliminate:
            paragraph_id = self.context.list_paragraph_id.pop(0)
            for word in m:
                if paragraph_id in m[word]:
                    m[word].pop(paragraph_id)
                if len(m[word]) == 0:
                    list_word_empty.append(word)
            for word in list_word_empty:
                if word in m:
                    m.pop(word)

    # Generate a batch of new paragraphs, which symbolizes the slow environmental 
    # changes in the recommendation system. If size_new_paragraph is too large relative 
    # to size_paragraph_pool, the machine learning model is difficult to predict
    def new_some_paragraph(self):
        a = self.game.count_word_per_paragraph
        b = self.game.size_new_paragraph
        word_count_need = a * b
        self.fill_list_buffer_word(word_count_need)
        for i in range(b):
            list_paragraph_word = self.context.list_buffer_word[i*a:(i+1)*a]
            paragraph_id = self.get_new_paragraph_id()
            self.add_to_map_word_paragraph(paragraph_id, list_paragraph_word)
            self.context.list_paragraph_id.append(paragraph_id)
        self.context.list_buffer_word = self.context.list_buffer_word[(i+1)*a:]
 
    # IMPORTANT!! Count the position of the word in the paragraph, and then use it to 
    # retrieve the word position relationship to determine whether the user will click or pay
    def add_to_map_word_paragraph(self, paragraph_id, list_paragraph_word):
        m = self.context.map_word_paragraph
        for position, word in enumerate(list_paragraph_word):
            if word not in m:
                m[word] = dict()
            if paragraph_id not in m[word]:
                m[word][paragraph_id] = list()
            m[word][paragraph_id].append(position)
    
    # Assign a new paragraph id
    def get_new_paragraph_id(self):
        if len(self.context.list_paragraph_id) == 0:
            return 1
        else:
            return self.context.list_paragraph_id[-1]

    # Fill `list_buffer_word` for subsequent batch generation of paragraphs
    def fill_list_buffer_word(self, word_count_need):
        while self.len_list_buffer_word < word_count_need:
            self.fill_list_buffer_word_one_corpus()
    
    # Divide an article, article and paragraph are completely different concepts
    def fill_list_buffer_word_one_corpus(self):
        path = self.list_corpus_path.pop(0)
        with open(path, 'r') as f:
            text = '\n'.join(list(f))
            list_word = self.text_to_list_word(text)
            self.context.list_buffer_word.extend(list_word)
    
    # All lowercase, no non-English letters, no numbers and punctuation, and word segmentation
    def text_to_list_word(self, text):
        text = text.lower()
        text = re.sub(r'</?\w+[^>]*>', ' ', text)
        text = re.sub('[^%s]' % re.escape(string.ascii_lowercase), ' ', text)
        text = re.sub('[%s]+' % re.escape(string.whitespace), ' ', text)
        text = text.strip()
        list_word = text.split(' ')
        return list_word
    
    # After each round of parsing the new corpus, the words are sorted according to 
    # the frequency of occurrence, and then used to generate `item` or `user`
    def rank_word(self):
        list_word_paragraph = list(self.context.map_word_paragraph.items())
        list_word_paragraph = sorted(list_word_paragraph,
            key=lambda x:len(x[1]), reverse=True)
        self.context.list_rank_word = [
            word_paragraph[0] for word_paragraph in list_word_paragraph
        ]
    
    # Whether the paragraph pool is full
    @property
    def paragraph_pool_is_full(self):
        return self.len_list_paragraph_id >= self.game.size_paragraph_pool

    # Is there a need to eliminate some of the original paragraphs
    @property
    def paragraph_pool_need_eliminate(self):
        return self.len_list_paragraph_id > self.game.size_paragraph_pool

    @property
    def len_list_paragraph_id(self):
        return len(self.context.list_paragraph_id)
    
    @property
    def len_list_buffer_word(self):
        return len(self.context.list_buffer_word)
        

    