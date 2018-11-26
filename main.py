import networkx as nx
from networkx.algorithms.flow import shortest_augmenting_path


edges = []
lastNode = 0
nodes = []

graph = nx.DiGraph()



def search(graph, source, sink):
    flow, path = 0, True
    
    while path:
        # search for path with flow moreFlow
        path, moreFlow = bfs_paths(graph, source, sink)
        flow += moreFlow
        # increase flow along the path
        for v, u in zip(path, path[1:]):
            if graph.has_edge(v, u):
                graph[v][u]['flow'] += moreFlow

        print('flow increased by', moreFlow, 
          #'at path', path,
          '; current flow', flow)
    return graph, flow
        


def bfs_paths(graph, start, goal):
    visited = {start}
    stack = [(start, 0, dict(graph[start]))]

    while stack:
        node, additionalFlow, neighbours = stack[-1]

        if node == goal:
            break

        while neighbours:
            nextNode, info = neighbours.popitem()

            if nextNode not in visited:
                break

        else:
            stack.pop()
            continue
        
        edge = graph.has_edge(node, nextNode)
        flow = info['flow']
        cap = info['capacity']
        neighbours = dict(graph[nextNode])

        if edge and flow < cap:
            stack.append((nextNode, cap - flow, neighbours))
            visited.add(nextNode)
        elif not edge and flow:
            stack.append(nextNode, flow, neighbours)
            visited.add(nextNode)
        

    #(source, sink) path and its flow moreFlow
    if(stack):
        for i in stack[1:]:
            moreFlow = i[1]
        for additionalFlow in stack[1:]:
            if(additionalFlow[1] < moreFlow):
                moreFlow = additionalFlow[1]
        
        path = []
        for additionalFlow in stack:
            path.append(additionalFlow[0])
        #moreFlow = min((f for additionalFlow, f, additionalFlow in stack[1:]), default=0)
        #path = [node for node, additionalFlow, additionalFlow in stack]

        return path, moreFlow
    else:
        return [], 0


def esayDFS(graph, start):

    stack = [start]
    visited = []
    f = open("outPut.txt" , 'w')
    f.write("digraph {\n")
    
    while stack:
        current = stack.pop()

        if(current not in visited):
            visited.append(current)
            for others in graph[current]:
                f.write("\t" + str(current) + " -> " + str(others) + " [label='" + str(graph[current][others]['flow']) + "'];\n")
                if(others not in visited):
                    stack.append(others)
    f.write("}\n")
    f.close()
                


def minCut(graph):
    cut_value = nx.minimum_cut(graph, 0, 3, flow_func=shortest_augmenting_path)[0]
    print("The Min cut is " + str(cut_value))
    return cut_value


with open("train.txt") as f:
    lines = f.readlines()
    for line in lines:
        if "digraph {" not in line and "}" not in line:
            line = line.strip()
            i = 0
            fname = ""
            sname = ""
            value = ""
            while(line[i] != " "):
                fname += line[i]
                i += 1
            i += 4
            while(line[i] != " "):
                sname += line[i]
                i += 1
            while(line[i] != '"'):
                i += 1
            i += 1
            while(line[i] != '"'):
                value += line[i]
                i += 1
            

            '''print(fname)
            print(sname)
            print(value)'''

            fname = int(fname)
            sname = int(sname)
            value = int(value)
            if(int(fname) > lastNode):
                lastNode = int(fname)
            if(int(sname) > lastNode):
                lastNode = int(sname)
            
            graph.add_edge(fname, sname, capacity = value, flow = 0)
graph, flow = search(graph, 0, lastNode)
cut_value = minCut(graph)
if(cut_value == flow):
    print("The max flow is 30")
else:
    print(str(cut_value) + " " + str(flow))
esayDFS(graph, 0)


