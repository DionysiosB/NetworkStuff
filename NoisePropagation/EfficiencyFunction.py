import networkx as nx
import sys
from itertools import izip
import numpy as np



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
		print 'current_vertex:',current_vertex
		CurrentVertexDistanceList=list(nx.single_source_shortest_path_length(G,current_vertex).values())
		print 'CurrentVertexDistanceList:',CurrentVertexDistanceList
		InverseDistanceList=ElementwiseInvertList(CurrentVertexDistanceList)
		print 'InverseDistanceList:',InverseDistanceList
		EfficiencySum+=sum(InverseDistanceList)
		print 'EfficiencySum:',EfficiencySum
		print '------------------------'
		
	AverageEfficiency=(1.0*EfficiencySum)/(N*(N-1))
	return AverageEfficiency

################################################################################################################################################
################################################################################################################################################
################################################################################################################################################

G=nx.star_graph(5)
R=EfficiencyComputation(G)
print R