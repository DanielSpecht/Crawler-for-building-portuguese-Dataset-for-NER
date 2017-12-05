#-*-encoding:UTF8-*-

# MULTIPROCESSING EXAMPLE

#http://sebastianraschka.com/Articles/2014_multiprocessing.html
#https://stackoverflow.com/questions/26520781/multiprocessing-pool-whats-the-difference-between-map-async-and-imap
#https://docs.python.org/3/library/multiprocessing.html

# import multiprocessing as mp
# def cube(x):
#     return x+1
# pool = mp.Pool(processes=4)
# results = [pool.apply(cube, args=(x,)) for x in range(1,7)]
# print(results)
# pool = mp.Pool(processes=4)

# e = pool.imap_unordered
# results1 = pool.imap(cube, range(1,10))
# results2 = e(func=cube,iterable=range(1,1000),chunksize=1)

# for i in results1:
#     print i

# for i in results2:
#     print i

# LOG EXAMPLE 1

# import logging
# FORMAT = '%(asctime)-15s %(clientip)s %(user)-8s %(message)s'
# logging.basicConfig(format=FORMAT)
# d = {'clientip': '192.168.0.1', 'user': 'fbloggs'}
# logger = logging.getLogger('tcpserver')
# logger.warning('Protocol problem: %s', 'connection reset', extra=d)

# LOG EXAMPLE 2

# import logging
# logger = logging.getLogger('myapp')
# hdlr = logging.FileHandler('./myapp.log')
# formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
# hdlr.setFormatter(formatter)
# logger.addHandler(hdlr) 
# logger.setLevel(logging.WARNING)

# logger.error('We have a problem')
# logger.info('While this is just chatty')



# FUNCTION 
# Erro mandando uma função criada com lambda para o multiprocessing
# https://pythontips.com/2013/08/04/args-and-kwargs-in-python-explained/
# https://stackoverflow.com/questions/8804830/python-multiprocessing-pickling-error

import itertools

class resource_cl():
    newid = itertools.count().next
    def __init__(self):
        #self.newid = itertools.count().next
        self.id = self.newid()
        #self.id = itertools.count().next()

a = resource_cl()
b = resource_cl()
c = resource_cl()

print (a.id)
print (b.id)
print (c.id)

a = ["a","b","c"]

i = iter(a)

while True:
    try:
        print i.next()
        
    except StopIteration:
        break



