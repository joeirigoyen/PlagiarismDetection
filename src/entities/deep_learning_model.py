from src.entities.model import Model
from src.entities.textdata import TextData, TextDataDirectory
from src.util.file_manager import get_max_len, get_list_texts
import tensorflow as tf
from tensorflow.keras.layers import Input, Dense, Dropout, Embedding, Conv1D, MaxPooling1D, GlobalMaxPooling1D, LSTM, concatenate
from tensorflow.keras.models import Model
from sklearn.model_selection import train_test_split
from sklearn.metrics import f1_score
from functools import partial


class DeepLearningModel(Model):
    def __init__(self, original_data: TextData | TextDataDirectory, suspicious_data: TextDataDirectory) -> None:
        super().__init__("deep_learning", original_data)
        self.suspicious_data = suspicious_data


    def check(self, loss_metric: str = "f1_score", optimizer: str  = "sgd") -> None:
        pass

    @staticmethod
    def train_model(original_data, suspicious_data) -> Model:

        f1_loss = partial(tf.keras.backend.binary_crossentropy, from_logits=True)

        def f1_metric(y_true, y_pred):
            return f1_score(y_true, y_pred.round())

        # Gather and preprocess data
        original_data.data.remove_punctuation()
        suspicious_data.data.remove_punctuation()
        texts = Model.get_list_texts(original_data.data) + Model.get_list_texts(suspicious_data.data)
        # Extract features
        tokenizer = tf.keras.preprocessing.text.Tokenizer()
        tokenizer.fit_on_texts(texts)
        sequences = tokenizer.texts_to_sequences(texts)
        maxlen = get_max_len(texts)
        features = tf.keras.preprocessing.sequence.pad_sequences(sequences, maxlen=maxlen)

        # Create training and test datasets
        labels = [0 for _ in range(len(original_data.data))] + [1 for _ in range(len(suspicious_data.data))]
        train_features, test_features, train_labels, test_labels = train_test_split(features, labels, test_size=0.2)

        # Build the machine learning model
        model = tf.keras.Sequential()
        model.add(Embedding(input_dim=len(tokenizer.word_index) + 1, output_dim=128, input_length=maxlen))
        model.add(Conv1D(64, kernel_size=3, activation='relu'))
        model.add(MaxPooling1D(pool_size=2))
        model.add(Conv1D(128, kernel_size=3, activation='relu'))
        model.add(GlobalMaxPooling1D())
        model.add(Dense(128, activation='relu'))
        model.add(Dropout(0.5))
        model.add(Dense(1, activation='sigmoid'))

        # Train the model
        model.compile(optimizer='sgd', loss=f1_loss, metrics=[f1_metric])
        model.fit(train_features, train_labels, epochs=10, batch_size=32, validation_data=(test_features, test_labels))

        # Evaluate the model
        test_f1 = f1_score(test_labels, model.predict(test_features).round())
        print('\nTest F1 score:', test_f1)
