import numpy as np
import time
from mpi4py import MPI
comm = MPI.COMM_WORLD
size = comm.Get_size()
rank = comm.Get_rank()

if rank == 0:
        data = np.arange(0,10000,0.01).reshape((1000, 1000))       
else:
        data = None

A = comm.bcast(data, root=0)

if rank == 0:
        ranges = [(0,100),(100,200),(200,300),(300,400),(400,500),(500,600),(600,700),(700,800),(800,900),(900,1000)]        
else:
        ranges = None

ranges = comm.scatter(ranges, root=0)

A = np.matrix(A)
#print A
#print " at rank %r A is of shape %r" %(rank,A.shape)
B = A.T[:,ranges[0]:ranges[1]]
#print " at rank %r B is of shape %r" %(rank,B.shape)
product = A * B
print " at rank %r product is of shape %r" %(rank,product.shape)
final_product = comm.gather(product, root=0)

if rank == 0:
	for i in range(10):
		if i > 0:
			C_2 = np.hstack((C_2,final_product[i]))
		else:
			C_2 = final_product[i]
	print "finished"
	print C_2.shape
	print " Final product rank :", C_2.shape
	print " Final product flatten :", C_2.flatten().shape
	dat = np.matrix(data) * np.matrix(data).T
	#print C_2.flatten()

	mse = mse = ((dat - C_2) ** 2).mean(axis=None)
	#mse = sum(dat.flatten() - C_2.flatten()) 
	print " Mean Square error : ",mse
