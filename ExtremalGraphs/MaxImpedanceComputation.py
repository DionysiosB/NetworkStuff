import networkx as nx
import sys
from itertools import izip
import numpy as np
import scipy.linalg as linalg

fin=open('InputGraphs.txt')

################################################################################################################################################
################################################################################################################################################
################################################################################################################################################
def MaxImpedanceComputation(InputGraph):
	
	MaxTotalImpedance=0
	
	G=InputGraph.copy()
	number_of_vertices=G.order()
	vertexlist=G.nodes()
	
	for top_node in vertexlist:
		for ground_node in vertexlist:
			if ground_node<top_node:
				ordered_vertexlist=vertexlist[:]
				ordered_vertexlist.remove(top_node)
				ordered_vertexlist.remove(ground_node)
				ordered_vertexlist.insert(0,top_node)
				ordered_vertexlist.insert(0,ground_node)
				
				LaplacianMatrix=nx.laplacian(G,ordered_vertexlist)
				ConductanceMatrix=np.delete(LaplacianMatrix,0,0)
				ConductanceMatrix=np.delete(ConductanceMatrix,np.s_[0],1)
				InputVector=[0]*(number_of_vertices-1)
				InputVector[0]=1
				VoltageVector=linalg.solve(ConductanceMatrix,InputVector)
				TotalImpedance=VoltageVector[0]
				if TotalImpedance>MaxTotalImpedance:
					MaxTotalImpedance=TotalImpedance
	
	return MaxTotalImpedance

################################################################################################################################################
################################################################################################################################################
################################################################################################################################################


max_impedance=0
#sentinel=0.0000000001

while True:
	current_line=fin.readline()
	current_graph_string=current_line.strip()
	if len(current_graph_string)==0:
		fin.close()
		NumericResultsFile=open('NumericResults.txt','a')
		NumericResultsFile.write(str(G.size()))
		NumericResultsFile.write('-')
		NumericResultsFile.write(str(max_impedance))
		NumericResultsFile.write(str('\n'))
		NumericResultsFile.close()
		break
	G=nx.parse_graph6(current_graph_string)
	test_impedance=MaxImpedanceComputation(G)
	if test_impedance>max_impedance:
		max_impedance=test_impedance