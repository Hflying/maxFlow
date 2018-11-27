import networkx as nx

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

        print("flow increased by " + str(moreFlow) + ": current flow " + str(flow))

    print("\n")
    print("The max Flow is " + str(flow))
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
        

    if(stack):
        for i in stack[1:]:
            moreFlow = i[1]
        for additionalFlow in stack[1:]:
            if(additionalFlow[1] < moreFlow):
                moreFlow = additionalFlow[1]
        
        path = []
        for additionalFlow in stack:
            path.append(additionalFlow[0])

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
                
def getCut(graph, start):
    g = graph.copy()

    stack = [start]
    visited = []
    
    while stack:
        current = stack.pop()

        if(current not in visited):
            visited.append(current)
            for others in g[current]:
                if(g[current][others]['flow'] == g[current][others]['capacity']):
                    continue
                else:
                    if(others not in visited):
                        stack.append(others)
    
    #print(visited)
    return visited

def minCut(graph, start, lastNode):
    cut = 0
    fromStart = getCut(graph, 0)
    fromEnd = getCut(graph, lastNode)
    for i in fromStart:
        for x in fromEnd:
            if(graph.has_edge(i, x) and i != x and x in fromEnd):
                cut +=  graph[i][x]['capacity']

    print("The min cut is " + str(cut))





with open("trainReal.txt") as f:
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
            
            fname = int(fname)
            sname = int(sname)
            value = int(value)
            if(int(fname) > lastNode):
                lastNode = int(fname)
            if(int(sname) > lastNode):
                lastNode = int(sname)
            
            graph.add_edge(fname, sname, capacity = value, flow = 0)

graph, flow = search(graph, 0, lastNode)
minCut(graph, 0, lastNode)

esayDFS(graph, 0)


