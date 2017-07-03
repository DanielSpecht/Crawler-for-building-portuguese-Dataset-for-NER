# -*- coding: utf-8 -*-
from __future__ import print_function
from keras.models import Sequential
from keras.models import Model
from keras.layers import Dense
from keras.preprocessing.text import Tokenizer
from keras.preprocessing.sequence import pad_sequences

from keras.layers import Embedding
from keras.layers import Dense
from keras.layers import Input
from keras.layers import Flatten
from keras.layers import Conv1D, MaxPooling1D, Embedding
from sklearn.metrics import (precision_score, recall_score, f1_score, accuracy_score)

from keras.utils import np_utils

import keras
import numpy


# fix random seed for reproducibility
#seed = 7
#numpy.random.seed(seed)
CLASSES = ["I-MISC","B-MISC","I-ORG","B-ORG","I-LOC","B-LOC","I-PER","B-PER","O"]
UNKNOWN_WORD = "@@@"
LINE_SENTENCE_END = ""
WINDOW_PADDING = 5
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

languages = ["dataSet","ned","esp"]

#dicionário indexando os arquivos dos idiomas
languageFileDictionary ={
    'dataSet':{"development":"dataSet","test":"ned.testb","train":"ned.train"},
    'ned':{"development":"ned.testa","test":"ned.testb","train":"ned.train"},
    'esp':{"development":"esp.testa","test":"esp.testb","train":"esp.train"}}
exception_verbosity="high"

targetTokenizer = Tokenizer(filters="",lower=False)
targetTokenizer.fit_on_texts(CLASSES)


for language in languages:

    print ("-------"+language+"-------")
    print ("Teste com uma janela de tamanho:%d"%(MAX_SEQUENCE_LENGTH))

    fileTrain = getFileLineList(languageFileDictionary[language]['train']);

    words = getWordList(fileTrain)

    targets = getClassificationList(fileTrain)

    inputTokenizer = Tokenizer(filters ="",lower=True)
    inputTokenizer.fit_on_texts(words)
    inputTokenizer.fit_on_texts([SENTENCE_DELIMITER])
    inputTokenizer.fit_on_texts([UNKNOWN_WORD])
    print('Encontrou %s palavras.' % len(inputTokenizer.word_index))

    chunks = getInputChunks(words,targets,inputTokenizer)

    inputSequences = getInputSequences(chunks,inputTokenizer)

    print('Encontrou %s classes.' % len(targetTokenizer.word_index))

    targetSequences = getTargetSequences(chunks,targetTokenizer)
    targetSequences = np_utils.to_categorical(targetSequences, 9)

    embedding_layer = Embedding(len(inputTokenizer.word_index) + 1, 64 , input_length=MAX_SEQUENCE_LENGTH)

    sequence_input = Input(shape=(MAX_SEQUENCE_LENGTH,), dtype='int64')
    embedded_sequences = embedding_layer(sequence_input)
    #64 feature maps, convolution de tamanho 3
    x = Conv1D(64, 2, activation='relu')(embedded_sequences)
    x = MaxPooling1D(pool_length=3, stride=3)(x)
    x = Flatten()(x)
    x = Dense(128, activation='relu')(x)
    preds = Dense(9, activation='softmax')(x)
    model = Model(sequence_input, preds)

    model.compile(loss='categorical_crossentropy', optimizer='rmsprop',metrics=['fmeasure','precision','recall'])


    #################################
    #DEBUG
    #################################
    fileTest = getFileLineList(languageFileDictionary[language]['test']);
    wordsTest = getWordList(fileTest)
    targetsTest = getClassificationList(fileTest)
    chunksTest = getInputChunks(wordsTest,targetsTest,inputTokenizer)
    inputSequencesTest = getInputSequences(chunksTest,inputTokenizer)
    targetSequencesTest = getTargetSequences(chunksTest,targetTokenizer)
    targetSequencesTest = np_utils.to_categorical(targetSequencesTest, 9)

    if True:
        target = open("DEBUG-INPUT", 'w')
        janelasTreino = numpy.array(chunks)[:,0]
        clasificacoesTreino = numpy.array(chunks)[:,1]
        #Averiguar as estruturas das windows
        for i in range(0,len(janelasTreino)):
            if clasificacoesTreino[i] != 'O':
                target.write("Chunks.Janela : "+ janelasTreino[i][0])
                target.write("\n")
                target.write("Chunks.Classificacao : "+ clasificacoesTreino[i])
                target.write("\n")
                target.write("Código no Tokenizer : "+str(inputTokenizer.word_index[janelasTreino[i][0]]))
                target.write("\n")
                target.write("Input na ANN : "+str(inputSequences[i][0]))
                target.write("\n")
                target.write("Output na ANN : "+str(targetSequences[i]))
                target.write("\n")
                #target.write(janelasTreino[i][0]+"--"+clasificacoesTreino[i]+"--"+str(inputTokenizer.word_index[janelasTreino[i][0]])+"====>"+"("+str(inputSequences[i][0])+str(targetSequences[i])+ ")"  )
                target.write("\n")

        target.close()

        target = open("DEBUG-OUTPUT", 'w')
        janelasTeste = numpy.array(chunksTest)[:,0]
        clasificacoesTeste= numpy.array(chunksTest)[:,1]
        #Averiguar as estruturas das windows DE TESTE
        for i in range(0,len(janelasTeste)):
            if clasificacoesTeste[i] != 'O':
                target.write("Chunks.Janela : "+ janelasTeste[i][0])
                target.write("\n")

                target.write("Chunks.Classificacao : "+ clasificacoesTeste[i])
                target.write("\n")
                target.write("Código no Tokenizer : "+str(inputTokenizer.word_index[janelasTeste[i][0]]))
                target.write("\n")
                target.write("Input na ANN : "+str(inputSequencesTest[i][0]))
                target.write("\n")
                target.write("Output na ANN : "+str(targetSequencesTest[i]))
                target.write("\n")
                #target.write(janelasTeste[i][0]+"--"+clasificacoesTeste[i]+"--"+str(inputTokenizer.word_index[janelasTeste[i][0]])+"====>"+"("+str(inputSequencesTest[i][0])+str(targetSequencesTest[i])+ ")"  )
                target.write("\n")
        target.close()
        model.summary()

        print ("Tipo array input : "+str(type(inputSequences)))
        print ("Shape array input : "+str(inputSequences.shape))
        print ("Tipo array classes : "+str(type(targetSequences)))
        print ("Shape array classes : "+str(targetSequences.shape))

        print (str(len(inputSequences)))
        print (str(len(targetSequences)))
        model.fit(inputSequences[:len(inputSequences)], targetSequences[:len(targetSequences)], batch_size=1024, nb_epoch=10, verbose=1, shuffle=False)

        predictions = model.predict(inputSequencesTest)

        truePositives = 0.0
        trueNegative = 0.0

        falsePositives = 0.0
        falseNegative = 0.0

        #print(">>>>")
        #print (targetTokenizer.word_index["O"])
        #print (targetTokenizer.word_index)
        #print (predictions[:20])
        for i in range(len(predictions)):
            max_prediction_index = 0
            max_prediction_value = 0.0

            for j in range(len(predictions[i])):
                if predictions[i][j] > max_prediction_value:
                    max_prediction_value = predictions[i][j]
                    max_prediction_index = j

            max_actual_index = 0
            max_actual_value = 0.0

            for j in range(len(targetSequencesTest[i])):
                if targetSequencesTest[i][j] > max_actual_value:
                    max_actual_value = targetSequencesTest[i][j]
                    max_actual_index = j


            #print (max_prediction_index)
            #print (max_actual_index)

            #false
            if max_prediction_index == (targetTokenizer.word_index["O"]-1):
                if max_prediction_index == max_actual_index:
                    trueNegative+=1.0
                else:
                    falseNegative+=1.0

            #true
            else:
                if max_prediction_index == max_actual_index:
                    truePositives+=1.0
                else:
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
        print(F)
