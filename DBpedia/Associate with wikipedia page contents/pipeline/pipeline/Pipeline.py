import os
import logging                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                         
import itertools
import multiprocessing as mp
from functools import reduce
#mp.util.log_to_stderr(mp.util.SUBDEBUG)

# TODOs 
# - Add an option to pass a dialect to the CsvOutputWriter
# - Put the validation functions in a Separate package, "Utils.py"
# - Logging raised exceptions informing the exact stage where it occured
# - Expose log file inside the stage
# - Order functions, private, public

# Functions are picklable if they are defined at the top-level of a module,
# This is required for calling a function using the process pools of the multiprocessing module
def _callPipelineFunc(call):
    """ Simply call the pipeline function to the recieved param """
    id = call[0]
    param = call[1]
    return Pipeline._Pipelines[id](param)

class Pipeline:
    """ The class that executes the stages recieved """
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
        def compose(f, g):
            """ functions f,g -> f(g()) """
            return lambda x: f(g(x))
        return reduce(compose, reversed(functions))

    def _buildPipelineFunction(self):
        """ Return the function built from all the steps of the pipeline and error logging """

        functions = self._getStagesFunctions()
        return self._createFunctionCompose(functions)    

    def _getStagesFunctions(self):
        """ Returns the stages "run" functions after adding exception logging for each stage """

        def addStageExceptLog(func,param,step):
            """ Logs the exceptions raised in stage """
            try:
                return func(param)
            except Exception as exception:
                logMsg = "ERROR in %s" % step.name
                return PipelineException()

        return [lambda param:addStageExceptLog(stage.run,param,stage) for stage in self.stages]

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

                if isinstance(result,PipelineException):                    
                    self.get = lambda: raiseExept(result)
                    print ("raiser")
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
            except:
                print ("A-ok")
                continue

    def _logExecution(self):
        """ Adds to the log the specifications of the Pipeline being run """
        logMsg = []

        def addLine(msg):
            logMsg.append(msg)
            logMsg.append("\n")

        addLine("\nExecuting pipeline: %s"% self.name)
        logMsg.append("%s has %s stages:\n"%(self.name,len(self.stages)))

        for idx,stage in enumerate(self.stages):
            addLine("--------------------")
            addLine("Stage %s : %s"%(idx+1,stage.name))
            addLine("--------------------")
            
            if stage.description:
                addLine("Description:\n%s"%stage.description)

        print (logMsg)
        self.logger.info(''.join(logMsg))

    def _initializeLog(self,logDir):
        if logDir:
            self.logger = logging.getLogger('pipeline')
            hdlr = logging.FileHandler(logDir)
            formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
            hdlr.setFormatter(formatter)
            self.logger.addHandler(hdlr)
            logging.basicConfig(level=logging.DEBUG)

class PipelineException(Exception):
    pass

class Stage:
    def __init__(self,
                 name,
                 description=""):

        self.name = name
        self.description = description

    def run(self,entry):
        pass

# class PipelineException(Exception):
#     pass

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

    class stage1(Stage):
        def run(self,entry):
            return str(entry) + "1"

    class stage2(Stage):
        def run(self,entry):
            raise Exception()
            return str(entry) + "2"
            #raise Exception("a")
            #return str(entry) + "2"

    stage1 =stage1(name="satge1", description="aaa")
    stage2 =stage2(name="satge2")

    stages = [stage1,stage2,stage2]

    pipeline = Pipeline(stages=stages,logPath="./tst.log",name = "PipeTest")

    for r in  pipeline.run(list(range(2))):
        print(r)

    print(pipeline.id)

    '''
    pipeline api

    step1 = CustomStep1()
    step2 = Custom step2()

    Pipeline.add(step1)
    Pipeline.add(step2)
    '''
