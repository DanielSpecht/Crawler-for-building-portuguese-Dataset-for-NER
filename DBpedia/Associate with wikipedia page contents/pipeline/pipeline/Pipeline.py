import os
import logging                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                         
import itertools
import multiprocessing as mp
from functools import reduce
import traceback

# TODOs 
# - Expose log file inside the stage
# - Order functions, private, public

# Functions are picklable if they are defined at the top-level of a module,
# This is required for calling a function using the process pools of the multiprocessing module
def _callPipelineFunc(call):
    """ Simply call the pipeline function to the recieved param """
    id = call[0]
    param = call[1]
    return Pipeline._Pipelines[id](param)

class PipelineException(Exception):
    """ Encapsulates the risen exceptions by the stages of the pipeline """
    def __init__(self,stage,pipeline,risenException):
        self.stage = stage
        self.pipeline = pipeline
        self.risenException = risenException

class Pipeline:
    """ Executes the stages recieved """
    _Pipelines = {}
    _generateId = itertools.count()

    def __init__(self,
                 name,
                 stages=[],
                 description=None,
                 threads=4,
                 chunkSize=1,
                 ordered=False,
                 logPath=None):
        
        self.stages = stages
        self.name = name
        self.description = description
        self.chunkSize = chunkSize
        self.ordered=ordered
        self.threads = threads
        self._initializeLog(logPath)
        self.id = next(self._generateId)

    def _createFunctionCompose(self,functions):
        def compose(f,g):
            """ functions f,g -> f(g()) """
            return lambda x: f(g(x))
        return reduce(compose, reversed(functions))

    def _buildPipelineFunction(self):
        """ Return the function built from all the steps of the pipeline and error logging """
        functions = self._getStagesFunctions()
        #functions = [stage.run for stage in self.stages ]

        return self._createFunctionCompose(functions)

    def _getStagesFunctions(self):
        """ Returns the stages "run" functions after adding exception logging for each stage """

        def addStageExceptLog(stage,position,param):
            """ Calls the stage 'run' function logging errors raised raised by the stage details """
            try:
                return stage.run(param)
            except Exception as exception:
                self._logStageException(stage,position,self,exception)
                return exception
        
        return [lambda param,stage=stage:addStageExceptLog(stage,position+1,param) for position,stage in enumerate(self.stages)]

    def run (self, entries):
        """ Runs the pipeline stages on the given entries"""

        self._logExecution()

        self._Pipelines[self.id] = self._buildPipelineFunction()
        pool = mp.Pool(processes=self.threads)
        executor = pool.imap if self.ordered else pool.imap_unordered
        class ExecutionResult:
            def __init__(self,result):
                
                def raiseExept(exeption):
                    raise exeption

                if isinstance(result,Exception):                   
                    self.get = lambda: raiseExept(result)
                else:    
                    self.get = lambda: result

        def getExecutionResults(executor):
            for result in executor:
                yield ExecutionResult(result)

        def pairEntriesPipeline(entries,pipelineId):
            """ Returns a tuple (entry,pipeline) """
            for entry in entries:
                yield (pipelineId,entry)

        for result in getExecutionResults(executor(func=_callPipelineFunc,iterable=pairEntriesPipeline(entries,self.id),chunksize=self.chunkSize)):
            try:
                yield result.get()
            except Exception:
                continue

    def _logStageException(self,stage,stageIndx,pipeline,stageException):
        logMsg = "Stage %s - %s raised an exception in Pipeline - %s"%(stageIndx,stage.name,pipeline.name)
        self.logger.exception(logMsg)

    def _logExecution(self):
        """ Adds to the log the specifications of the Pipeline being run """
        logMsg = []

        logMsg.append("Executing pipeline: %s"% self.name)
        logMsg.append("%s has %s stages:\n"%(self.name,len(self.stages)))

        for idx,stage in enumerate(self.stages):
            logMsg.append("--------------------")
            logMsg.append("Stage %s : %s"%(idx+1,stage.name))
            logMsg.append("--------------------")
            
            if stage.description:
                logMsg.append("Description:\n%s"%stage.description)
    
        self.logger.info('\n'.join(logMsg))

    def _initializeLog(self,logDir):
        if logDir:
            self.logger = logging.getLogger('pipeline')
            hdlr = logging.FileHandler(logDir)
            formatter = logging.Formatter('\n%(asctime)s %(levelname)s \n\n %(message)s')
            hdlr.setFormatter(formatter)
            self.logger.addHandler(hdlr)
            logging.basicConfig(level=logging.DEBUG)

class Stage:
    def __init__(self,
                 name,
                 description=""):
        self.name = name
        self.description = description

    def run(self,entry):
        pass

class PipelineException(Exception):
     pass

if __name__ == '__main__':
    
    # tests for csv Writer

    # test csv output writer

    # file = "names.csv"
    # fieldnames = ['first_name', 'last_name']

    # writer = CsvOutputWriter(outputPath=file,wipe=True,fieldNames=fieldnames)
    # writer.writeRow({'first_name': 'Baked', 'last_name': 'Beans, deliciouss'})
    # writer.writeRow({'first_name': 'Lovely', 'last_name': 'Spam'})
    # writer.writeRow({'first_name': 'Wonderful', 'last_name': 1})
  
    # # teste - averiguar como os inteiros sao armazenados
    # with open(file, 'rb') as csvfile:
    #     spamreader = csv.reader(csvfile)
    #     for row in spamreader:
    #         print ', '.join(row)
    #         print row

    #pipeline = Pipeline(["names.csv"],workspaceDir="./workspace")
    # stage_1 = PipelineSummation()
    # stage_2 = PipelineMultiplication()
    # stages = [stage_1,stage_2]
    #pipeline = Pipeline(stages=stages)
    #pipeline.run()

    class tst:
        def run(self):
            return 1

    class stage1(Stage):
        def run(self,entry):
            #print ("STAGE 1 EXECUTING")
            #raise PipelineException()
            return entry**2

    class stage2(Stage):
        def run(self,entry):
            #print ("STAGE 2 EXECUTING")
            #raise Exception("Exception message")
            return str(entry) + "2"
            #return str(entry) + "2"

    stage1 =stage1(name="stage1", description="aaa")
    stage2 =stage2(name="stage2")

    
    n = 2

    stages = []
    for i in list(range(n)):
        stages.append(stage1)

    #pipelined = Pipeline(stages=stages,logPath="./tst.log",name = "PipeTest",chunkSize=500)
    pipelined = Pipeline(stages=stages,logPath="./tst.log",name = "PipeTest",chunkSize=5000)

    b = 10**6
    import time
    time1 = time.time()
    for r in  pipelined.run(list(range(b))):
        pass
    time2 = time.time()
    print (' function took %0.3f ms' % ( (time2-time1)*1000.0))
    
    time1 = time.time()

    for i in  list(range(b)):
        for j in list(range(n)):
            stage1.run(i)
    time2 = time.time()
    print (' function took %0.3f ms' % ( (time2-time1)*1000.0))

    print("2")

    print(pipelined.id)
