#!/usr/bin/env python3

#  Copyright (c) 2019, Cameron Hochberg
#  All rights reserved.
#
# Author: Cameron Hochberg
# Date: 07/2019
# Homepage: https://github.com/Susanou
# Email: cam.hochberg@gmail.com
#

import sys
import os
import matplotlib.pyplot as plt
import argparse
import time
import pandas as pd
import numpy as np
import joblib
import urllib

from bs4 import BeautifulSoup
from mpl_toolkits.mplot3d import Axes3D
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import SGDClassifier
from sklearn.naive_bayes import MultinomialNB as naive
from sklearn.naive_bayes import BernoulliNB
from sklearn.naive_bayes import ComplementNB # as naive
from sklearn.svm import SVC as svc
from sklearn.model_selection import GridSearchCV
from sklearn.linear_model import Perceptron
from sklearn.pipeline import Pipeline
from sklearn.datasets import load_files
from sklearn.model_selection import train_test_split
from sklearn import metrics

dataset = load_files("src/sentiment/data")
docs_train, docs_test, y_train, y_test = train_test_split(
    dataset.data, dataset.target, test_size=.99, random_state=42, shuffle=True)
vectorizer = TfidfVectorizer(ngram_range=(1,1), analyzer='word', use_idf=True)

def get_page(url: str):
    """Fonction pour recuperer le texte nettoyer d'une page html
    
    Parameters
    ----------
    url : str
        Url de la page
    
    Returns
    -------
    str
        Renvoi le texte de la page sans le code HTML
    """
    response = urllib.request.urlopen("%s" % url)
    html = response.read()
    soup = BeautifulSoup(html, "html5lib")
    text = soup.get_text(strip=True)

    return text

def predictSGD(): 
    if not os.path.isfile("sentiment/sgd_model.plk"):
        start = time.time()

        clf = Pipeline([
            ('vect', vectorizer),
            ('clf', SGDClassifier(loss='log', penalty='l2',
                            alpha=1e-3, random_state=42,
                            max_iter=5, tol=None))
        ], verbose=True)

        parameters = {
            'vect__ngram_range': [(1, 1), (1, 2), (1,3), (1,4), (1,5)],
            
            'clf__alpha': (1e-2, 1e-3, 5e-3, 7e-3, 4e-3, 3e-3, 2e-3, 8e-3, 9e-3),
        }

        gs_clf = GridSearchCV(clf, parameters, cv=5, iid=False, n_jobs=-1)
        gs_clf.fit(docs_train, y_train)

        print(gs_clf.best_params_)

        y_predicted = gs_clf.predict(docs_test)

        print("END...... total=%0.2f s" %(start-time.time()))

        # Print the classification report
        print(metrics.classification_report(y_test, y_predicted,
                                            target_names=dataset.target_names))

        cm = metrics.confusion_matrix(y_test, y_predicted)
        print(cm)


        plt.matshow(cm, cmap=plt.cm.jet)
        #plt.show()

        joblib.dump(gs_clf, "sgd_model.plk")
        return gs_clf
    else:
        return joblib.load("sentiment/sgd_model.plk")


#If using SVC, not able to get the the different proba of each case
def predictedSVC():

    if not os.path.isfile("sentiment/svc_model.plk"):

        start = time.time()

        clf = Pipeline([
            ('vect', vectorizer),
            ('clf', svc(tol=1e-3, verbose=0, random_state=42,
                C=1.0, max_iter=-1, gamma='scale', probability=True))
        ], verbose = True)

        parameters={
            'vect__ngram_range': [(1, 1), (1, 2), (1,3), (1,4), (1,5)],
            'clf__tol':(1e-3, 1e-2, 5e-3, 2e-3, 3e-3,4e-3),
            'clf__gamma':('auto', 'scale'),
            'clf__C':(1.0,.1,.2,.3,.4, 0.5, 0.6, 0.7, 0.8, 0.9)
        }

        gs_clf = GridSearchCV(clf, parameters, cv=5, iid=False, n_jobs=-1)
        gs_clf.fit(docs_train, y_train)

        y_predicted = gs_clf.predict(docs_test)

        print(gs_clf.best_params_)

        print("End.......... total=%.2f s" % (start - time.time()))

        # Print the classification report
        print(metrics.classification_report(y_test, y_predicted,
                                            target_names=dataset.target_names))

        cm = metrics.confusion_matrix(y_test, y_predicted)
        print(cm)


        plt.matshow(cm, cmap=plt.cm.jet)
        #plt.show()

        joblib.dump(gs_clf, "svc_model.plk")
        return gs_clf
    else:
        return joblib.load("sentiment/svc_model.plk")

def predictNaiveBayes():

    if not os.path.isfile("sentiment/naive_model.plk"):

        start = time.time()

        #MultinomialNB Pipeline
        clf = Pipeline([
            ('vect', vectorizer),
            ('clf', naive(alpha=1.0, fit_prior=True))
        ], verbose=True)

        parameters={
            'vect__ngram_range': [(1, 1), (1, 2), (1,3), (1,4), (1,5)],
            'clf__fit_prior': (True, False),
            'clf__alpha': (1.0, 0.1, 0.5, 2.0, .25, 0.75, 0.002),
        }

        gs_clf = GridSearchCV(clf, parameters, cv=5, iid=False, n_jobs=-1)
        gs_clf.fit(docs_train, y_train)

        print(gs_clf.best_params_)

        y_predicted = gs_clf.predict(docs_test)

        print("End.......... total=%.2f s" % (start - time.time()))

        # Print the classification report
        print(metrics.classification_report(y_test, y_predicted,
                                            target_names=dataset.target_names))

        cm = metrics.confusion_matrix(y_test, y_predicted)
        print(cm)

        plt.matshow(cm, cmap=plt.cm.jet)
        #plt.show()


        joblib.dump(gs_clf, "naive_model.plk")

        return gs_clf
    else:
        return joblib.load("sentiment/naive_model.plk")

def get_sentiment():
    return dataset.target_names

def vote(prob1, prob2, prob3):
    """Fonction nous permettant de voter sur le resulat en cas d'absence de choix
    
    Parameters
    ----------
    prob1 : array-like
        liste de probabilite pour chaque classe selon le premier algorithme
    prob2 : array-like
        liste de probabilite pour chaque classe selon le deuxieme algorithme
    prob3 : array-like
        liste de probabilite pour chaque classe selon le troisieme algorithme
    
    Returns
    -------
    int
        Renvoi soit l'indexe du resultat du resultat le plus probable
    float
        La  probabilite associee au resultat
    """

    top1 = np.argsort(prob1, axis=1)[:,-2:]
    top2 = np.argsort(prob2, axis=1)[:,-2:]
    top3 = np.argsort(prob3, axis=1)[:,-2:]

    top1 = top1[0]
    top2 = top2[0]
    top3 = top3[0]

    sums = dict()
        
    for i in top1:
        if i in sums:
            sums[i] += prob1[0][i]
        else:
            sums[i] = prob1[0][i]
    for j in top2:
        if j in sums:
            sums[j] += prob2[0][j]
        else:
            sums[j] = prob2[0][j]
    for k in top3:
        if k in sums:
            sums[k] += prob3[0][k]
        else:
            sums[k] = prob3[0][k]

    maxV = max(sums.values())
    maxK = [k for k, v in sums.items() if v == maxV]

    return (maxK[0], maxV)