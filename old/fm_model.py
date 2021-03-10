# coding=utf8
import tensorflow as tf
from hyper_param import HyperParam
from example_manager import ExampleManager

class FmModel(tf.keras.Model):

    def __init__(self, embedding_dim=8):
        super(FmModel, self).__init__()
        self.embedding_dim = embedding_dim
        self.bucket_size = 100_000
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

if __name__ == '__main__':
    em = ExampleManager(HyperParam())
    batch_size = 32
    train_ds = em.example_to_dataset(loop_count=1, batch_size=batch_size)
    val_ds = em.example_to_dataset(loop_count=2, batch_size=batch_size)
    model = FmModel(embedding_dim=8)
    model.compile(
        optimizer=tf.keras.optimizers.Adam(learning_rate=0.001),
        loss=tf.keras.losses.BinaryCrossentropy(from_logits=True),
        metrics=[tf.keras.metrics.AUC()]
    )
    model.fit(train_ds, epochs=1)
    loss, auc = model.evaluate(val_ds)
    print('auc', auc)
    # print(train_ds.take(1).as_numpy_iterator().next())