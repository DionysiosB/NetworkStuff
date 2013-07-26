import networkx as nx
import sys
from itertools import izip
import numpy as np
import scipy.linalg as linalg

fin=open('InputGraphs.txt')

################################################################################################################################################
################################################################################################################################################
################################################################################################################################################
def ElementwiseInvertList(InputList):
	InputList.remove(0)
	return [1.0/x for x in InputList]

################################################################################################################################################
################################################################################################################################################
################################################################################################################################################
def EfficiencyComputation(InputGraph):
	
	G=InputGraph.copy()
	N=G.order()
	vertexlist=G.nodes()
	
	EfficiencySum=0.0
	for current_vertex in vertexlist:
		CurrentVertexDistanceList=list(nx.single_source_shortest_path_length(G,current_vertex).values())
		InverseDistanceList=ElementwiseInvertList(CurrentVertexDistanceList)
		EfficiencySum+=sum(InverseDistanceList)
		
	AverageEfficiency=(1.0*EfficiencySum)/(N*(N-1))
	return AverageEfficiency

################################################################################################################################################
################################################################################################################################################
################################################################################################################################################

maximum_efficiency=0
sentinel=0.00000001

while True:
	current_line=fin.readline()
	current_graph_string=current_line.strip()
	if len(current_graph_string)==0:
		AllResultsFile=open('AllResults.g6','a')
		AllResultsFile.write(str(CurrentGraph6String))
		AllResultsFile.write(str('\n'))
		AllResultsFile.close()
		fin.close()
		break
	G=nx.parse_graph6(current_graph_string)
	current_efficiency=EfficiencyComputation(G)
	if current_efficiency>=maximum_efficiency-sentinel:
		CurrentGraph6String=current_graph_string
		maximum_efficiency=current_efficiency
		print current_graph_string
		optimal_graph=G.copy()
