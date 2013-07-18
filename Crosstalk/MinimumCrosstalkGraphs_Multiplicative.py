import networkx as nx

############################################################################################################################################################
############################################################################################################################################################
############################################################################################################################################################
def MinimumMultiplicativeCrosstalkGraphFinder(number_of_vertices,number_of_edges):
	
	if number_of_edges<number_of_vertices-1:
		print 'Too few edges. The graph will be disconnected. Exiting...'
		return -1
	
	
	G=nx.star_graph(number_of_vertices-1)
	remaining_edges=number_of_edges-number_of_vertices+1
	
	for current_vertex in range(2,number_of_vertices):
		if remaining_edges<=0:break
		for previous_vertex in range(1,current_vertex):
			G.add_edge(previous_vertex,current_vertex)
			remaining_edges-=1
			if remaining_edges<=0:break
	
	return G

############################################################################################################################################################
############################################################################################################################################################
############################################################################################################################################################

testGraph=MinimumMultiplicativeCrosstalkGraphFinder(10,25)
print 
print testGraph.nodes()
print '------------------------------------------------------------------'
print testGraph.edges()
print testGraph.degree()