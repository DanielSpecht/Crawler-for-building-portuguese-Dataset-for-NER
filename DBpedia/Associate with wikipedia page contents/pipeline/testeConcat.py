def _buildPipelineFunction (functions):
    print len(functions)
    if len(functions) == 1:
        print "ok"
        return functions[0]

    # abc cba
    else:
        def funcConcat(f1,f2,inpt):
            return f2(f1(inpt))
        
        print "olar"
        del functions[0:2]
        functions.insert(0,funcConcat)
        return _buildPipelineFunction(functions)

def teste2(functions,input):
    for f in functions:
        input = f(input)
    return input

def a(s):
    return s+"a"

def b(s):
    return s+"b"

def c(s):
    return s+"c"

def d(s):
    return s+"d"

funcs = [a,b,c,d]
print teste2(funcs,"")
#print _buildPipelineFunction(funcs)("")