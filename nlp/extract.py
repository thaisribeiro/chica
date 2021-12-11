import json
import random
import pathlib
import numpy as np
import pickle
import nltk
from nltk.stem import WordNetLemmatizer
from keras.models import load_model

path = pathlib.Path(__file__).parent.resolve()
lemmatizer = WordNetLemmatizer()
words = pickle.load(open(f'{path}/words.pkl', 'rb'))
classes = pickle.load(open(f'{path}/classes.pkl', 'rb'))
model = load_model(f'{path}/model.h5')
intents_json = json.loads(open(f'{path}/intents.json').read())

def clear_writing(writing):
    sentence_words = nltk.word_tokenize(writing)
    return [lemmatizer.lemmatize(word.lower()) for word in sentence_words]


def bag_of_words(writing, words):
    sentence_words = clear_writing(writing)
    bag = [0]*len(words)
    for setence in sentence_words:
        for i, word in enumerate(words):
            if word == setence:
                bag[i] = 1

    return(np.array(bag))


def class_prediction(writing):
    prevision = bag_of_words(writing, words)
    response_prediction = model.predict(np.array([prevision]))[0]

    results = [[index, response] for index, response in enumerate(
        response_prediction) if response > 0.25]

    if "1" not in str(prevision) or len(results) == 0:
        results = [[0, response_prediction[0]]]

    results.sort(key=lambda x: x[1], reverse=True)
    return [{"intent": classes[r[0]], "probability": str(r[1])} for r in results]


def get_response(intents):
    tag = intents[0]['intent']
    list_of_intents = intents_json['intents']
    for idx in list_of_intents:
        if idx['tag'] == tag:
            result = idx['responses']
            context = idx['context']
            tag = idx['tag']

            if len(idx['responses']) > 1:
                result = random.choice(idx['responses'])

            return result, context, tag
