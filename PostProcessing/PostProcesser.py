# -*- coding: utf-8 -*-
import nltk.data
import os, nltk
import string
import json
import re

def main ():

    with open('../G1/ArticlesCrawled.json', 'r') as f:
        json_articles = json.load(f)

        setLocationEntities(json_articles)
        setPersonEntities(json_articles)
        processParagraphs(json_articles)
        generateFile(json_articles)


        #Save#
        with open('ArticlesProcessed.json', 'w') as f:
            f.write(json.dumps(json_articles))

def setLocationEntities (articles):
    for article in articles:
        for entity in article["Entities"]:
            if "/cidade/" in entity["Page"]:
                entity["Type"] = "LOC"

def setPersonEntities (articles):
    #Get the list of known politicians
    politicians = {}
    with open('../G1/PoliticiansFiltered.json') as data_file:
        for politician in json.load(data_file):
            politicians[politician["Page"]] = politician

    for article in articles:
        for entity in article["Entities"]:
            if entity["Page"] in politicians:
                entity["Type"] = "PER"
                entity["Names"] = [politician["FullName"],politician["ShortName"]]

def processParagraphs(articles):
    segmentSentences(articles)
    removeUndesiredCharacters(articles)

def segmentSentences(articles):
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
            article["Text"][i] = article["Text"][i].replace("\n", "")
            article["Text"][i] = article["Text"][i].replace("\r", "")
            article["Text"][i] = article["Text"][i].replace("\t", "")
            article["Text"][i] = article["Text"][i].replace("\v", "")
        print article["Text"]



if __name__ == "__main__":
    main()
