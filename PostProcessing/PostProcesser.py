# -*- coding: utf-8 -*-
import nltk.data
import os, nltk
import string
import json
import re
import itertools


IOB = { "Inside":"I - ", "Outside":"O", "Begin":"B - "}
TYPES = {"Person":"PER", "Location":"LOC", "Organization":"ORG"}

def main ():

    with open('../G1/ArticlesCrawled.json', 'r') as f:
        json_articles = json.load(f)

        #json_articles = json_articles[:100]
        setLocationEntities(json_articles)
        setPersonEntities(json_articles)
        removeUnsetEntities(json_articles)
        processParagraphs(json_articles)
        generateDataSet(json_articles)

        with open('ArticlesProcessed.json', 'w') as f:
            f.write(json.dumps(json_articles))

def setLocationEntities (articles):
    for article in articles:
        for entity in article["Entities"]:
            if "/cidade/" in entity["Page"]:
                entity["Type"] = TYPES["Location"]

def setPersonEntities (articles):
    #Get the list of known politicians
    politicians = {}
    with open('../G1/PoliticiansFiltered.json') as data_file:
        for politician in json.load(data_file):
            politicians[politician["Page"]] = politician

    for article in articles:
        for entity in article["Entities"]:
            if entity["Page"] in politicians:
                entity["Type"] = TYPES["Person"]
                entity["Names"] = [politicians[entity["Page"]]["FullName"],politicians[entity["Page"]]["ShortName"]]

def removeUnsetEntities(articles):
    for article in articles:
        for entity in reversed(article["Entities"]):
            if not entity["Type"]:
                article["Entities"].remove(entity)

def processParagraphs (articles):
    segmentSentences(articles)
    removeUndesiredCharacters(articles)

def segmentSentences (articles):
    sentence_tokenizer=nltk.data.load('tokenizers/punkt/portuguese.pickle')
    for article in articles:
        sentences = []
        for paragraph in article["Text"]:
            sentences = sentences + sentence_tokenizer.tokenize(paragraph[0])
        article["Text"] = sentences

#This function presumes that "segment sentences" has been run on the data
def removeUndesiredCharacters(articles):
    for article in articles:
        #for sentence in article["Text"]:
        for i in range(len(article["Text"])):
            article["Text"][i] = article["Text"][i].replace("\n", " ")
            article["Text"][i] = article["Text"][i].replace("\r", " ")
            article["Text"][i] = article["Text"][i].replace("\t", " ")
            article["Text"][i] = article["Text"][i].replace("\v", " ")

def generateDataSet(articles):
    dataSet = open('dataSet', 'w')

    for article in articles:
        writeArticleURL(article,dataSet)
        for sentence in article["Text"]:
            words = nltk.word_tokenize(sentence)
            sequenceOfEntityTerms = []
            annotatedSentence = []
            entitiesWords = map( lambda x: getEntityWords(x) , article["Entities"])
            entitiesWords = list(itertools.chain.from_iterable(entitiesWords))

            for word in words:
                if word in entitiesWords:
                    sequenceOfEntityTerms.append(word)

                #If this word does not indicate the end of a sequence:
                else:
                    if sequenceOfEntityTerms:
                        annotatedSentence += attributeSequenceToEntities(sequenceOfEntityTerms,article["Entities"])
                        sequenceOfEntityTerms = []
                    annotatedSentence.append([word, IOB["Outside"]])

            #Special case: The sentence ends with the named entity
            if sequenceOfEntityTerms:
                annotatedSentence += attributeSequenceToEntities(sequenceOfEntityTerms,article["Entities"])
                sequenceOfEntityTerms = []

            writeAnnotadedSentence(annotatedSentence,dataSet)
            #printAnnotadedSentence(annotatedSentence)

    dataSet.close()

def writeArticleURL(article,dataSetFile):
    dataSetFile.write(article["URL"]+"\n")

def writeAnnotadedSentence(sentence,dataSetFile):
    for annotation in sentence:
        #dataSetFile.write(annotation[0].encode("UTF-8")+"\t"+annotation[1].encode("UTF-8")+"\n")
        dataSetFile.write(annotation[0]+"\t"+annotation[1]+"\n")
    dataSetFile.write("\n")

def printAnnotadedSentence(sentence):
    for annotation in sentence:
        print (annotation)
        #print (annotation[0]+"--"+annotation[1])


def attributeSequenceToEntities (sequence,entities):
    maxScore = 0
    maxScoreEntity = None

    for entity in entities:
        score = 0
        entityWords = getEntityWords(entity)

        for word in sequence:
            if word in entityWords:
                score += 1
                if score > maxScore:
                    maxScore = score
                    maxScoreEntity = entity
            else:
                break

    annotatedSequence = [[]]*maxScore

    #Special cases: sequences begining or ending with qords not starting with uppercase
    #i.e. "de Carlos de Almeida da Silva" "de Carlos de Almeida da Silva de da"
    i = 0
    j = maxScore-1

    print ("\n")
    print ("Sequence:"+str(sequence))
    print ("Annotaded sequence:"+str(annotatedSequence))
    print ("MaxScore:"+str(maxScore))

    print ("HOOY -- "+str(len(sequence)))
    while  i < maxScore and (not sequence[i][0].isupper()) :
        print (str(i)+"--"+str(maxScore-1))
        annotatedSequence[i] = [sequence[i],IOB["Outside"]]
        i+=1
        print ("OIE")

    if i == maxScore:
        return annotatedSequence

    while j > 0 and (not sequence[j][0].isupper()):
        annotatedSequence[j] = [sequence[j],IOB["Outside"]]
        j-=1

    annotatedSequence[i] = [sequence[i],IOB["Begin"]+maxScoreEntity["Type"]]
    i+=1

    print ("range--"+str(i)+"-"+str(j+1))
    for k in range(i,j+1):
        annotatedSequence[k] = [sequence[i],IOB["Inside"]+maxScoreEntity["Type"]]

    #Se a entidade mais compatível não cobre toda a sequência
    if maxScore != len(sequence):
        annotatedSequence += attributeSequenceToEntities(sequence[maxScore:],entities)

    return annotatedSequence

def getEntityWords(entity):
    words =[]
    for name in entity["Names"]:
        words += name.split()

    return words

            #words = nltk.word_tokenize(sentence)
            #annotatedSentence = []
            #lastEntityFound = None

            #for word in words:
            #    tagType = "O"
            #    tagPrefix = ""
            #    wordIsEntity = False
            #    for entity in article["Entities"]:
            #        if entity["Type"]:
            #            #i.e. entity["Names"] = ["Marcos Camargo","Marquinhos"]
            #            for name in entity["Names"]:
            #                #i.e. nameTerm = "Marcos", "Camargo", "Marquinhos"
            #                for nameTerm in name.split():
            #                    if word == nameTerm:
            #                        tagType = entity["Type"]
            #                        wordIsEntity = True
            #                        if lastEntityFound is not entity :
            #                            tagPrefix = "B - "
            #                            lastEntityFound = entity
            #                        else:
            #                            tagPrefix ="I - "

            #    if not wordIsEntity:
            #        lastEntityFound = None

            #    print word+"---"+tagPrefix+tagType
            #    annotatedSentence.append([word,tagPrefix+tagType])


if __name__ == "__main__":
    main()
