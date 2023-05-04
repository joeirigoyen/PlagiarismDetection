from src.entities.model import Model
import tensorflow as tf
from tensorflow.keras.layers import Input, Dense, Dropout, Embedding, Conv1D, MaxPooling1D, LSTM, concatenate
from tensorflow.keras.models import Model


class DeepLearningModel(Model):
    def __init__():
        pass

    def check(self, loss_metric: str = "f1_score", optimizer: str  = "sgd") -> None:
        pass

    @staticmethod
    def train_model() -> Model:
        pass
        """ input1 = Input(shape=(MAX_SEQUENCE_LENGTH,))
        input2 = Input(shape=(MAX_SEQUENCE_LENGTH,))
        embedding_layer = Embedding(MAX_NUM_WORDS, EMBEDDING_DIM)
        sequence_encoding = embedding_layer(input1)
        sequence_encoding = Dropout(0.2)(sequence_encoding)
        sequence_encoding = Conv1D(64, 5, activation='relu')(sequence_encoding)
        sequence_encoding = MaxPooling1D(pool_size=4)(sequence_encoding)
        sequence_encoding = LSTM(64)(sequence_encoding)
        sequence_encoding = Model(inputs=input1, outputs=sequence_encoding)

        pattern_encoding = embedding_layer(input2)
        pattern_encoding = Dropout(0.2)(pattern_encoding)
        pattern_encoding = Conv1D(64, 5, activation='relu')(pattern_encoding)
        pattern_encoding = MaxPooling1D(pool_size=4)(pattern_encoding)
        pattern_encoding = LSTM(64)(pattern_encoding)
        pattern_encoding = Model(inputs=input2, outputs=pattern_encoding)

        merged = concatenate([sequence_encoding.output, pattern_encoding.output])
        merged = Dense(64, activation='relu')(merged)
        merged = Dropout(0.2)(merged)
        merged = Dense(1, activation='sigmoid')(merged)
        model = Model(inputs=[sequence_encoding.input, pattern_encoding.input], outputs=merged)

        # Compile the model
        model.compile(loss='binary_crossentropy', optimizer='adam', metrics=['accuracy'])

        # Train the model
        model.fit([x_train_1, x_train_2], y_train, validation_data=([x_val_1, x_val_2], y_val), epochs=10, batch_size=64)

        # Evaluate the model
        score, acc = model.evaluate([x_test_1, x_test_2], y_test, batch_size=64)

        # Use the model to detect plagiarism
        new_document = preprocess_text(new_document)
        numerical_data = convert_to_numerical(new_document)
        plagiarism_score = model.predict(numerical_data) """
