import numpy as np
import time
from mpi4py import MPI
comm = MPI.COMM_WORLD
rank = comm.Get_rank()

if rank==0:
	print "Starting Process"
	A = np.arange(0,10000,0.01).reshape((1000, 1000))
	A = np.matrix(A)
	B = A.T
	print " sending B matrix across"
	comm.send(B[:,100:200], dest=1, tag=21)
	comm.send(B[:,200:300], dest=2, tag=21)
	comm.send(B[:,300:400], dest=3, tag=21)
	comm.send(B[:,400:500], dest=4, tag=21)
	comm.send(B[:,500:600], dest=5, tag=21)
	comm.send(B[:,600:700], dest=6, tag=21)
	comm.send(B[:,700:800], dest=7, tag=21)
	comm.send(B[:,800:900], dest=8, tag=21)
	comm.send(B[:,900:1000], dest=9, tag=21)
	print "receiving product"
	C_dic = {}
	C_dic[0] = A * B[:,0:100]
	C_dic[1] = comm.recv(source=1, tag=22)
	C_dic[2] = comm.recv(source=2, tag=22)
	C_dic[3] = comm.recv(source=3, tag=22)
	C_dic[4] = comm.recv(source=4, tag=22)
	C_dic[5] = comm.recv(source=5, tag=22)
	C_dic[6] = comm.recv(source=6, tag=22)
	C_dic[7] = comm.recv(source=7, tag=22)
	C_dic[8] = comm.recv(source=8, tag=22)
	C_dic[9] = comm.recv(source=9, tag=22)
	print "Assembleing the matrix"
	for i in range(10):
		if i > 0:
			C_2 = np.hstack((C_2,C_dic[i]))
		else:
			C_2 = C_dic[i]
	print "job done"

else:
	print "Starting slave node :", rank
	A = np.arange(0,10000,0.01).reshape((1000, 1000))
	A = np.matrix(A)

	B_part = comm.recv(source=0, tag=21)
	C_part = A * np.matrix(B_part)
	comm.send(C_part, dest=0, tag=22)



