# coding=utf8
import os
import json
import tensorflow as tf

class ExampleManager(object):
    def __init__(self, hyper_param):
        self.hyper_param = hyper_param

        self.preclk_example_message_queue = []
        self.postclk_example_message_queue = []
    
    def init_example_dir_condition(self, loop_count):
        self.init_example_dir()
        if loop_count <= 1:
            self.remove_all_example()

    @property
    def example_dir_path(self):
        return self.hyper_param.k_example_dir_path
    
    def get_preclk_example_path(self, loop_count):
        path = os.path.join(self.example_dir_path, 'preclk_example_%04d.example.txt' % loop_count)
        return path
    
    def init_example_dir(self):
        if not os.path.exists(self.example_dir_path):
            os.mkdir(self.example_dir_path)

    def remove_all_example(self):
        for name in os.listdir(self.example_dir_path):
            if not name.endswith('.example.txt'):
                continue
            path = os.path.join(self.example_dir_path, name)
            os.remove(path)

    def emit_preclk_example(self, example_data):
        self.preclk_example_message_queue.append(example_data)

    def dump_example_in_queue(self, loop_count):
        path = self.get_preclk_example_path(loop_count)
        with open(path, 'w') as fw:
            while len(self.preclk_example_message_queue) > 0:
                example_data = self.preclk_example_message_queue.pop(0)
                fw.write(json.dumps(example_data))
                fw.write("\n")


    def example_to_dataset(self, loop_count, batch_size=32, shuffle=True):
        labels = []
        feature_input = dict(
            f_uid=[],
            f_tid=[]
        )
        path = self.get_preclk_example_path(loop_count)
        with open(path, 'r') as f:
            for line in f:
                example_data = json.loads(line.strip())
                labels.append(example_data['label'])
                feature_input['f_uid'].append(str(example_data['f_uid']))
                feature_input['f_tid'].append(str(example_data['f_tid']))
        ds = tf.data.Dataset.from_tensor_slices((feature_input, labels))
        if shuffle:
            ds = ds.shuffle(buffer_size=len(labels))
        ds = ds.batch(batch_size)
        return ds