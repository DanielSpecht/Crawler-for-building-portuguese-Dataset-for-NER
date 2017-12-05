import os
import sys
import argparse

def _validDirectory(dirPath):
    if not os.path.isdir(dirPath):
        msg = "The directory %r does not exist."%(dirPath)
        raise argparse.ArgumentTypeError(msg)
    return dirPath

def _validFile(filePath):
    if not os.path.isfile(filePath):
        msg = "The file %r does not exist." % filePath
        raise argparse.ArgumentTypeError(msg)
    return filePath

def _avoidFileOverride(documents,outputPath):
    try:
        for document in documents:
            documentName = os.path.basename(document)
            futureDocumentPath = os.path.join(outputPath,documentName)
            if os.path.isfile(futureDocumentPath):
                msg = "The path %r already exists.\nNo averride allowed.\nTo allow override use the flag --wipe."%(futureDocumentPath)
                raise argparse.ArgumentError(None,msg)

    except argparse.ArgumentError as error:
        print error.message
        sys.exit(1)

def addDefaultArguments(parser):
    """ Parses the default arguments for the pipeline, required for every step"""
    parser.add_argument('--files', '-f',
                        type=_validFile,
                        required=True,
                        nargs='+',
                        help='CSV files containing a column which is a Wikipedia page.')

    parser.add_argument('--wipe', '-w',
                        action='store_true',
                        help='If there are files in the specified output path with the same name as the files produced, erase them. An exception will be raise if there are files with the same name in the directory and the wipe is flag not sent.')

    parser.add_argument('--log', '-l',
                        action='store_true',
                        help='Create a log for the operations.')

    parser.add_argument('--output', '-o',
                        type=_validDirectory,
                        required=True,
                        nargs=1,
                        help='The path where the output files will be saved.')