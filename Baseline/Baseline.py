# -*- coding: utf-8 -*-
from __future__ import division
from __future__ import print_function
from keras.models import Sequential
from keras.models import Model
from keras.layers import Dense
from keras.preprocessing.text import Tokenizer
from keras.preprocessing.sequence import pad_sequences

from time import time

from keras.layers import Embedding
from keras.layers import Dense
from keras.layers import Input
from keras.layers import Flatten
from keras.layers import Conv1D, MaxPooling1D, Embedding
from sklearn.metrics import (precision_score, recall_score, f1_score, accuracy_score)

from keras.utils import np_utils

import keras
import numpy


#svm
from sklearn import datasets
from sklearn import svm


# fix random seed for reproducibility
#seed = 7
#numpy.random.seed(seed)
CLASSES = ["I-MISC","B-MISC","I-ORG","B-ORG","I-LOC","B-LOC","I-PER","B-PER","O"]
UNKNOWN_WORD = "@@@"
LINE_SENTENCE_END = ""
WINDOW_PADDING = 4
SENTENCE_DELIMITER = "***"
MAX_SEQUENCE_LENGTH = 2*WINDOW_PADDING+1

#IGNORABLE_WORDS = ["","-DOCSTART-"]

def getFileLineList( filePath ):
    return open(filePath,'r').read().splitlines()

def getClassificationList( fileLineArray ):
    classifications = list()
    for i, s in enumerate(fileLineArray):
        # pega ultima palavra
        if(len(fileLineArray[i].rsplit(' ', 1))>1):
            classifications.append(fileLineArray[i].rsplit(' ', 1)[1])
        else:
            classifications.append(LINE_SENTENCE_END)
    return classifications

def getWordList( fileLineArray ):
    words = list()
    for i, s in enumerate(fileLineArray):
        # pega a primeira palavra
        if(len(fileLineArray[i].split())>1):
            words.append(fileLineArray[i].split()[0])
        else:
            words.append(LINE_SENTENCE_END)
    #return map(lambda x: x.lower(), words)
    return map(lambda x:x.lower(), words)
    inputSequences = list()
    for i in range( 0,len(inputs)):
        inputInstance = tokenizer.texts_to_sequences(inputs[i])
        inputInstance = numpy.array(inputInstance).ravel()
        inputSequences.append(inputInstance)
    return numpy.array(inputSequences)

def getTargetSequences(chunks,targetTokenizer):
    targets = numpy.array(chunks)[:,1]
    targetSequences = targetTokenizer.texts_to_sequences(targets)
    targetSequences = numpy.array(targetSequences).flatten()
    targetSequences = numpy.array(map(lambda x: x-1, targetSequences))
    return targetSequences

def getInputSequences(chunks,tokenizer):

    inputs = numpy.array(chunks)[:,0]
    inputSequences = list()
    for i in range( 0,len(inputs)):
        inputInstance = tokenizer.texts_to_sequences(inputs[i])
        inputInstance = numpy.array(inputInstance).ravel()
        inputSequences.append(inputInstance)
    return numpy.array(inputSequences)

def getInputChunks(wordList,clasificationsList, inputTokenizer):
    chunks = list()
    for i in range(0,len(wordList)):
        chunk = list()

        if wordList[i] != LINE_SENTENCE_END:

            if wordList[i] not in inputTokenizer.word_index:
                chunk.append(UNKNOWN_WORD)
            else:
                chunk.append(wordList[i])

            for leftIndex in range(i-1,i-WINDOW_PADDING-1,-1):
                if leftIndex < 0:
                    chunk.insert(0,SENTENCE_DELIMITER)
                elif wordList[leftIndex]==LINE_SENTENCE_END:
                    for _ in range(leftIndex,i-WINDOW_PADDING-1,-1):
                        chunk.insert(0,SENTENCE_DELIMITER)
                    break
                else:
                    if wordList[leftIndex] not in inputTokenizer.word_index:
                        chunk.insert(0,UNKNOWN_WORD)
                    else:
                        chunk.insert(0,wordList[leftIndex])

            for rightIndex in range(i+1,i+WINDOW_PADDING+1):
                if  rightIndex>len(wordList)-1 :
                    chunk.append(SENTENCE_DELIMITER)
                elif wordList[rightIndex]==LINE_SENTENCE_END:
                    for _ in range(rightIndex,i+WINDOW_PADDING+1):
                        chunk.append(SENTENCE_DELIMITER)
                    break
                else:
                    if wordList[rightIndex] not in inputTokenizer.word_index:
                        chunk.append(UNKNOWN_WORD)
                    else:
                        chunk.append(wordList[rightIndex])

            chunks.append([chunk,clasificationsList[i]])

    return chunks




#class Conll2002(object):
#
#    def __init__(self, filePath):
#        self.filePath = filePath
#
#    def setDictionary(dictionary = None):
#        if dictionary:
#            return
#
#
#
#    def getOutput():
#
#        return



languages = ["ned","esp"]

#dicionário indexando os arquivos dos idiomas
languageFileDictionary ={
    'ned':{"development":"ned.testa","test":"ned.testb","train":"ned.train"},
    'esp':{"development":"esp.testa","test":"esp.testb","train":"esp.train"}}
exception_verbosity="high"

targetTokenizer = Tokenizer(filters="",lower=False)
targetTokenizer.fit_on_texts(CLASSES)




for language in languages:

    print ("-------"+language+"-------")
    print ("Teste com uma janela de tamanho:%d"%(MAX_SEQUENCE_LENGTH))


    fileTrain = getFileLineList(languageFileDictionary[language]['train'])

    print ("getFileLineList")
    print (fileTrain[:10])

    words = getWordList(fileTrain)
    print ("getWordList")
    print (words[:10])

    targets = getClassificationList(fileTrain)
    print ("getClassificationList")
    print (targets[:10])

    inputTokenizer = Tokenizer(filters ="",lower=True)

    #Creates the grammar of known words
    inputTokenizer.fit_on_texts(words)
    inputTokenizer.fit_on_texts([SENTENCE_DELIMITER])
    inputTokenizer.fit_on_texts([UNKNOWN_WORD])
    print('Encontrou %s palavras.' % len(inputTokenizer.word_index))

    chunks = getInputChunks(words,targets,inputTokenizer)

    inputSequences = getInputSequences(chunks,inputTokenizer)

    print('Encontrou %s classes.' % len(targetTokenizer.word_index))


    targetSequences = getTargetSequences(chunks,targetTokenizer)
    #targetSequences = np_utils.to_categorical(targetSequences, 9)

    #digits = datasets.load_digits()
    #print ("========= DIGITS ==========")
    #print ("INPUT")
    #print (digits.data)
    #print ("OUTPUT")
    #print(digits.target)

    #print ("========= WORDS ==========")
    #print ("INPUT")
    #print (inputSequences)
    #print ("OUTPUT")
    #print(targetSequences[:20])


    clf = svm.SVC()
    clf = svm.SVC(gamma=0.001, C=100)
    X,y = inputSequences, targetSequences

    t0 = time()
    print ("Training")
    print (len(X))
    clf.fit(X,y)
    print("done in %0.3fs" % (time() - t0))

    #################################
    #TEST
    #################################
    fileTest = getFileLineList(languageFileDictionary[language]['test']);
    wordsTest = getWordList(fileTest)
    targetsTest = getClassificationList(fileTest)
    chunksTest = getInputChunks(wordsTest,targetsTest,inputTokenizer)
    inputSequencesTest = getInputSequences(chunksTest,inputTokenizer)
    targetSequencesTest = getTargetSequences(chunksTest,targetTokenizer)
    targetSequencesTest = np_utils.to_categorical(targetSequencesTest, 9)

    targetSequencesTest = targetSequencesTest
    inputSequencesTest = inputSequencesTest
    truePositives = 0.0
    trueNegative = 0.0

    falsePositives = 0.0
    falseNegative = 0.0

    for i in range(len(inputSequencesTest)):
        x = [inputSequences[i]]
        y = targetSequences[i]

        prediction = clf.predict(x)[0]

        #print ("False")
        #print (targetTokenizer.word_index["O"])

        if y != prediction:
            print ("Prediction")
            print (prediction)
            print ("Actual")
            print (y)


        if 0 == prediction:
            if prediction == y:
                #print("tn")
                trueNegative+=1.0
            else:
                #print("fn")
                falseNegative+=1.0

        else:
            if prediction == y:
                #print("tp")
                truePositives+=1.0
            else:
                #print("fp")
                falsePositives+=1.0

    B = 1.0
    F = ((1.0+B*B)*truePositives) / ((1.0+B*B)*truePositives + B*B*falseNegative+falsePositives)
    print ("tp")
    print(truePositives)
    print ("tn")
    print(trueNegative)
    print ("fp")
    print(falsePositives)
    print ("fn")
    print(falseNegative)


    print ("F")
    print (F)
