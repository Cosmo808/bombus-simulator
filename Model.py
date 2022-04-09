from tensorflow.keras.models import Model
from tensorflow.keras.layers import Dense, Input, Dropout
from tensorflow.keras import optimizers, losses


class DNN:

    def __init__(self, state_size, action_size, lr, gamma):
        self.state_size = state_size
        self.action_size = action_size
        self.lr = lr
        self.epsilon = 0.9
        self.gamma = gamma
        self.q_eval = None
        self.q_next = None
        self.model_eval = Model()
        self.model_targ = Model()
        self._dnn_generate()

    def _dnn_generate(self):
        # evaluation net
        eval_inputs = Input(shape=(self.state_size, ))
        x = Dense(64, activation='relu')(eval_inputs)
        x = Dropout(rate=0.5)(x)
        x = Dense(32, activation='relu')(x)
        self.q_eval = Dense(self.action_size, activation='sigmoid')(x)
        self.model_eval = Model(eval_inputs, self.q_eval)

        # target net
        target_inputs = Input(shape=(self.state_size, ))
        x = Dense(64, activation='relu')(target_inputs)
        x = Dropout(rate=0.5)(x)
        x = Dense(32, activation='relu')(x)
        self.q_next = Dense(self.action_size, activation='sigmoid')(x)
        self.model_targ = Model(target_inputs, self.q_next)

        # compile
        self.model_eval.compile(
            optimizer=optimizers.RMSprop(learning_rate=self.lr),
            loss=losses.mean_squared_error,
            metrics=['accuracy']
        )
        self.model_targ.compile(
            optimizer=optimizers.RMSprop(learning_rate=self.lr),
            loss=losses.mean_squared_error,
            metrics=['accuracy']
        )

    def target_replace_op(self):
        w_e = self.model_eval.get_weights()
        self.model_targ.set_weights(w_e)
        print("params has changed")
