from django.shortcuts import render, redirect
import joblib
import sklearn
import numpy as np  # linear algebra
import pandas as pd  # data processing
from django.contrib import messages
import string
import nltk
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from django.contrib.auth.decorators import login_required

pipeline = joblib.load('./pipeline.sav')


@login_required(login_url='/')
def index(request):
    if request.method == 'POST':
        title = str(request.POST.get('title'))
        text = str(request.POST.get('details'))
        query_text = [remove_punctuation_stopwords_lemma(title + text)]
        prediction = pipeline.predict(query_text)

        if prediction[0] == 0:
            messages.error(
                request, 'This may be a Fake News.')
            return redirect('index')
        else:
            messages.success(
                request, 'This may be a Real News.')
            return redirect('index')

    return render(request, 'detector/index.html')


def remove_punctuation_stopwords_lemma(sentence):
    filter_sentence = ''

    # Remove punctuation
    all_list = [char for char in sentence if char not in string.punctuation]
    clean_str = ''.join(all_list)

    # Remove stopwords
    stop = stopwords.words('english')
    clean_str = ' '.join([word for word in clean_str.split() if word not in (stop)])

    # Lemmatization
    lemmatizer = WordNetLemmatizer()
    words = nltk.word_tokenize(clean_str)  # tokenization
    for word in words:
        filter_sentence = filter_sentence + ' ' + \
            str(lemmatizer.lemmatize(word)).lower()
    return filter_sentence
