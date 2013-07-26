import networkx as nx

############################################################################################################################################################
############################################################################################################################################################
############################################################################################################################################################
def MaxDistanceGraphFinder(number_of_vertices,number_of_edges):
	
	if number_of_edges<number_of_vertices-1:
		print 'Too few edges. The graph will be disconnected. Exiting...'
		return -1
	if number_of_edges>(number_of_vertices-1)*number_of_vertices/2.0:
		print 'Too many edges. Such a graph cannot exist. Exiting...'
		return -1
	
	
	G=nx.path_graph(number_of_vertices)
	remaining_edges=number_of_edges-number_of_vertices+1
	
	for current_vertex in range(2,number_of_vertices):
		if remaining_edges<=0:break
		for previous_vertex in range(current_vertex-1):
			G.add_edge(previous_vertex,current_vertex)
			remaining_edges-=1
			if remaining_edges<=0:break
	
	return G

############################################################################################################################################################
############################################################################################################################################################
############################################################################################################################################################

testGraph=MaxDistanceGraphFinder(6,11)
print 
print testGraph.nodes()
print '------------------------------------------------------------------'
print testGraph.edges()
print testGraph.degree()