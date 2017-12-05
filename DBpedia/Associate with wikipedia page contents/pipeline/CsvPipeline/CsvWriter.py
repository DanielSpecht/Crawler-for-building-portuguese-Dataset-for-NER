import os

'''
This class Aims to describe the configurations of a csv file
'''
class CsvFileConfiguration:
    def __init__(self,
                 fileName,
                 csvDelimiter=',',
                 csvQuotechar='"'):

        self.fileName = fileName
        self.csvDelimiter = csvDelimiter
        self.csvQuotechar = csvQuotechar         

'''
This class is responsible for writing a csv output incrementally
Defines the polcies for result writing
'''
class CsvOutputWriter:
    def __init__(self,
                 outputPath,
                 fieldNames,
                 wipe=False):

        self.wipe = wipe
        self.outputPath = outputPath
        self.fieldNames = fieldNames
        
        #self._validDirectory(self.outputPath)

        if not wipe: # Do not override
            self._avoidFileOverride(self.outputPath)
        
        elif os.path.isfile(outputPath): # Delete file if exists
            os.unlink(outputPath)

        # Set csv file header
        self._writeHeader()

    def _writeHeader(self):
        with open(self.outputPath, 'a') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=self.fieldNames)
            writer.writeheader()

    def writeRow(self,row):
        with open(self.outputPath, 'a') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames= self.fieldNames)
            writer.writerow(row)

    def readFileTuples(self,filePath, delimiter=' ',quotechar='|'):
        with open(filePath, 'rb') as csvfile:
            reader = csv.reader(iterable=csvfile, delimiter=delimiter,quotechar=quotechar)
            for row in reader:
                pass

    def _avoidFileOverride(self,outputPath):
        if os.path.isfile(outputPath):
            msg = "The path %r already exists.\nNo averride allowed.\nTo allow override use the flag wipe."%(outputPath)
            raise CsvOutputWriterException(msg)

class CsvOutputWriterException(Exception):
    pass