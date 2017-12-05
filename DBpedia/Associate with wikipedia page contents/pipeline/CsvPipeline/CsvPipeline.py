import os

class CsvPipeline(Pipeline):
    def __init__(self,
                 csvInputFiles,
                 workspaceDir,
                 stages=[],
                 name=None,
                 description=None,
                 wipe=False,
                 log=False,
                 maxWorkers=100):

        Pipeline.__init__(self,stages=stages,name=name,description=description,wipe=wipe,log=log,maxWorkers=maxWorkers)
        map(self._validFile,csvInputFiles) # Validate file paths

    def _validFile(self,filePath):
        if not os.path.isfile(filePath):
            msg = "The file %r does not exist." % filePath
            raise PipelineException(msg)

    def _validDirectory(self,outputPath):
        dirPath = os.path.dirname(outputPath)
        if dirPath=="": # If it's in the same folder
            return
        if not os.path.isdir(dirPath):
            msg = "The directory %r does not exist."%(dirPath)
            raise PipelineException(msg)

    # def _runOnFile(self,filePath):
        
    #     outputPath = self.outputfolder + os.path.basename(filePath) # same name as the input file
    #     writer = CsvOutputWriter(outputPath=outputPath,wipe=True,fieldNames=fieldnames)

    #     with open(filePath,"r") as csvFile:
    #         reader = csv.reader(csvfile, delimiter=self.csvDelimiter, quotechar=self.csvQuotechar)
    #         for result in ThreadPool(self.maxWorkers).imap_unordered(self._runStagesOnRow, reader):
    #             yield result


