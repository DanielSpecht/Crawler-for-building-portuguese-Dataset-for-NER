import argparse
import csv
import sys
import os
# def appendWikipediaPages():
import concurrent




executor = thread.ThreadPoolExecutor(max_workers=10)
a = executor.submit(my_function)

def AttachWikipediaPageInfo(documents):
    for document in documents:
        with open('eggs.csv', 'rb') as csvfile:
            reader = csv.reader(csvfile, delimiter=' ', quotechar='|')
            for row in reader:
                print ', '.join(row)

        for line in lines:
            yield appendWikipediaPage()

def validDirectory(path):
    if not os.path.isdir(path):
        msg = "%r is not an existing directory" % path
        raise argparse.ArgumentTypeError(msg)
    return path

def validFile(path):
    if not os.path.isfile(path):
        msg = "%r is not an existing file" % path
        raise argparse.ArgumentTypeError(msg)
    return path

def avoidFileOverride(documents,outputPath):
    try:
        for document in documents:
            documentName = os.path.basename(document)
            futureDocumentPath = os.path.join(outputPath,documentName)
            if os.path.isfile(futureDocumentPath):
                msg = "The path %r already exists.\nNo averride allowed.\nTo allow override use the flag --wipe." % futureDocumentPath
                raise argparse.ArgumentError(None,msg)

    except argparse.ArgumentError as error:
        print error.message
        sys.exit(1)


#def validFile(path):

if __name__ == "__main__":
    parser = argparse.ArgumentParser(prog='WikiInfoAttach',description='Attach Wikipedia page contents to csv file')
    
    # --files
    parser.add_argument('--files','-f',
                        type = validFile,
                        required=True,
                        nargs='+',
                        help='CSV files containing a column which is a Wikipedia page.')
    # --wipe
    parser.add_argument('--wipe','-w',
                        action='store_true',
                        help='If there are files in the specified output path with the same name as the files produced, erase them. An error will be raise if there are files with the same name in the directory and the wipe flag not set.')
    # --output path
    parser.add_argument('--output','-o',
                        type =validDirectory,
                        required=True,
                        nargs=1,
                        help='The path where the output files will be saved.')
    # --column of link
    parser.add_argument('--column','-c',
                        required=True,
                        nargs=1,
                        help='The column of the csv which specifies the wikipedia page.')


    args = parser.parse_args()
    
    avoidFileOverride(args.files,args.output[0])


    
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
    #python getWikipediaPage.py --files input/file.txt --output  --column aa