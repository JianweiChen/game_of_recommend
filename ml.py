# coding=utf8
import tensorflow as tf
from base import Base

# Factory Machine model for retrieval
class FmModel(tf.keras.Model):
    def __init__(self):
        super().__init__()
    
    def call(self, x):
        pass

# Deep Factory Machine model for retrieval
class DeepFmModel(tf.keras.Model):
    def __init__(self, embedding_dim=8, bucket_size=50_000):
        super().__init__()
        self.embedding_dim = embedding_dim
        self.bucket_size = bucket_size
        fc_uid = tf.feature_column.categorical_column_with_hash_bucket(
            'f_uid', hash_bucket_size=self.bucket_size)
        fc_tid = tf.feature_column.categorical_column_with_hash_bucket(
            'f_tid', hash_bucket_size=self.bucket_size)
        self.user_embedding_layer = tf.keras.layers.DenseFeatures([
            tf.feature_column.embedding_column(fc_uid, self.embedding_dim)])
        self.item_embedding_layer = tf.keras.layers.DenseFeatures([
            tf.feature_column.embedding_column(fc_tid, self.embedding_dim)])
        self.dot_layer = tf.keras.layers.Dot(axes=(1,1))
        self.output_layer = tf.keras.layers.Dense(1, activation='sigmoid')
    
    def call(self, x):
        yu = self.user_embedding_layer(x)
        yt = self.item_embedding_layer(x)
        y_uxt = self.dot_layer([yu, yt])
        y = self.output_layer(y_uxt)
        return y

# Deep Factory Machine model for retrieval
class DeepFmRegressionModel(tf.keras.Model):
    def __init__(self):
        super().__init__()
    
    def call(self, x):
        pass

class ModelManager(Base):
    
    def __init__(self, game):
        super().__init__(game)

        self.model_retrieval = FmModel()
        self.model_click = DeepFmModel()
        self.model_pay = DeepFmRegressionModel()
        
        self.compile_retrieval_model()
        self.compile_click_model()
        self.compile_pay_model()
    
    # Clear the tensorflow model dumped to the hard disk
    def remove(self):
        #todo
        pass

    def train(self):
        self.train_retrieval_model()
        self.train_click_model()
        self.train_pay_model()

    def compile_click_model(self):
        learning_rate = self.game.model_click_adam_learning_rate
        self.model_click.compile(
            optimizer=tf.keras.optimizers.Adam(learning_rate=learning_rate),
            loss=tf.keras.losses.BinaryCrossentropy(from_logits=True),
            metrics=[tf.keras.metrics.AUC()]
        )

    def compile_retrieval_model(self):
        pass

    def compile_pay_model(self):
        pass

    def train_click_model(self):
        list_example_click = self.game.example_manager.load_example_click(self.context.loop)
        ds = self.example_to_dataset(list_example_click, batch_size=self.game.model_click_batch_size)
        history=self.model_click.fit(ds, epochs=1, verbose=0)
        # print(history.history)
        self.context.map_summary['loss_click'] = history.history['loss']
        self.context.map_summary['auc_click'] = history.history['auc']
        if self.game.model_click_extra_train_epochs:
            self.model_click.fit(ds, epochs=self.game.model_click_extra_train_epochs, verbose=0)

    def train_pay_model(self):
        pass

    def train_retrieval_model(self):
        pass

    def predict_click(self, uid, list_tid):
        model = self.model_click
        return self._predict(model, uid, list_tid)
    
    def _predict(self, model, uid, list_tid, batch_size=32):
        feature_input = dict(
            f_uid=[],
            f_tid=[]
        )
        for tid in list_tid:
            feature_input['f_uid'].append(str(uid))
            feature_input['f_tid'].append(str(tid))
        ds = tf.data.Dataset.from_tensor_slices(feature_input)
        ds = ds.batch(batch_size)
        list_predict_array = model.predict(ds)
        list_predict_score = [x[0] for x in list_predict_array]
        list_tid_score = list(zip(list_tid, list_predict_score))
        return list_tid_score
        

    def example_to_dataset(self, list_example_data, batch_size=32, shuffle=True):
        labels = []
        feature_input = dict(
            f_uid=[],
            f_tid=[]
        )
        for example_data in list_example_data:
            labels.append(example_data['label'])
            feature_input['f_uid'].append(str(example_data['f_uid']))
            feature_input['f_tid'].append(str(example_data['f_tid']))
        ds = tf.data.Dataset.from_tensor_slices((feature_input, labels))
        if shuffle:
            ds = ds.shuffle(buffer_size=len(labels))
        ds = ds.batch(batch_size)
        return ds
