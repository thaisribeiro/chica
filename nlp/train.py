import os
import pathlib
import json
import pickle
import nltk
import random
import numpy as np

from nltk.stem import WordNetLemmatizer
from keras.models import Sequential
from keras.layers import Dense, Activation, Dropout
from tensorflow.keras.optimizers import SGD

path = pathlib.Path(__file__).parent.resolve()


with open(os.path.join(path, 'classes.pkl'), 'w') as fp:
    pass
with open(os.path.join(path, 'words.pkl'), 'w') as fp:
    pass
with open(os.path.join(path, 'model.h5'), 'w') as fp:
    pass

nltk.download('punkt')
nltk.download('wordnet')

lemmatizer = WordNetLemmatizer()

def train():
    words = []
    documents = []
    intents = json.loads(open(f'{path}/intents.json').read())
    classes = [i['tag'] for i in intents['intents']]
    ignore_words = ["!", "@", "#", "$", "%", "*", "?"]

    for intent in intents['intents']:
        for pattern in intent['patterns']:
            word = nltk.word_tokenize(pattern)
            words.extend(word)
            documents.append((word, intent['tag']))

    words = [lemmatizer.lemmatize(w.lower())
             for w in words if w not in ignore_words]

    words = sorted(list(set(words)))
    classes = sorted(list(set(classes)))

    pickle.dump(words, open(f'{path}/words.pkl', 'wb'))
    pickle.dump(classes, open(f'{path}/classes.pkl', 'wb'))

    training = []
    output_empty = [0] * len(classes)
    for document in documents:
        bag = []
        pattern_words = document[0]
        pattern_words = [lemmatizer.lemmatize(
            word.lower()) for word in pattern_words]
        for word in words:
            bag.append(1) if word in pattern_words else bag.append(0)

        output_row = list(output_empty)
        output_row[classes.index(document[1])] = 1

        training.append([bag, output_row])

    random.shuffle(training)
    training = np.array(training)

    x = list(training[:, 0])
    y = list(training[:, 1])

    model = Sequential()
    model.add(Dense(128, input_shape=(len(x[0]),), activation='relu'))
    model.add(Dropout(0.5))
    model.add(Dense(64, activation='relu'))
    model.add(Dropout(0.5))
    model.add(Dense(len(y[0]), activation='softmax'))

    sgd = SGD(lr=0.01, decay=1e-6, momentum=0.9, nesterov=True)
    model.compile(loss='categorical_crossentropy', optimizer=sgd, metrics=['accuracy'])

    m = model.fit(np.array(x), np.array(y), epochs=200, batch_size=5, verbose=1)

    model.save(f'{path}/model.h5', m)
    print('finish.')
    return 'finish'
    

train()
