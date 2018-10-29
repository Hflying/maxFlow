import networkx as nx


edges = []
lastNode = 0
nodes = []

graph = nx.DiGraph()



def search(graph, source, sink):
    flow, path = 0, True
    
    while path:
        # search for path with flow reserve
        path, reserve = bfs_paths(graph, source, sink)
        flow += reserve
        # increase flow along the path
        for v, u in zip(path, path[1:]):
            if graph.has_edge(v, u):
                graph[v][u]['flow'] += reserve
            else:
                graph[u][v]['flow'] -= reserve
        print('flow increased by', reserve, 
          'at path', path,
          '; current flow', flow)
    return graph
        


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
        

    # (source, sink) path and its flow reserve
    reserve = min((f for additionalFlow, f, additionalFlow in stack[1:]), default=0)
    path = [node for node, additionalFlow, additionalFlow in stack]
    
    return path, reserve


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
graph = search(graph, 0, lastNode)
esayDFS(graph, 0)


