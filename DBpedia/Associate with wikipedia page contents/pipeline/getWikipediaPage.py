import argparse
import csv
import sys
import os
import thread
import concurrent
import pipeline

#executor = thread.ThreadPoolExecutor(max_workers=10)
#a = executor.submit(my_function)

def attachWikipediaPageInfo(documents):
    for document in documents:
        with open('eggs.csv', 'rb') as csvfile:
            reader = csv.reader(csvfile, delimiter=' ', quotechar='|')
            for row in reader:
                print ', '.join(row)

def streamLines():
    pass

def _validateWikipediaColumn(filePath,columnName):
    """ Checks if the column containing the wikipedia page link exists """
    pass

if __name__ == "__main__":
    parser = argparse.ArgumentParser(prog='WikiInfoAttach', 
                                     description='Attach Wikipedia page contents to csv file')

    pipeline.addDefaultArguments(parser)

    parser.add_argument('--column', '-c',
                        required=True,
                        nargs=1,
                        help='The column of the csv which specifies the wikipedia page.')

    args = parser.parse_args()

    print args
       

    # TODO - 15/11
    # Output - add a fileless option?
    # pattern https://stackoverflow.com/questions/3898572/what-is-the-standard-python-docstring-format
    #TODO - Atributes
    # csv attributes

    #TODO - Erros
    # requests.exceptions.ConnectionError
    # wikipedia.exceptions.PageError: <exception str() failed>
    # [OK] directory does not exist
    # [OK] file does not exist
    # [OK] files with the same name in the directory
    
    # file open

    #test : 
    #python getWikipediaPage.py --files /home/daniel/Repositories/NERDataSetBuilder/DBpedia/entity_extraction/Person/Person_1.csv --output  --column aa