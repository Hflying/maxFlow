import networkx as nx


edges = []
lastNode = 0
nodes = []

graph = nx.DiGraph()

def search(graph, start, end):
    flow = 0
    path = True
    
    path = bfs_paths(graph, start, end)

    while path:
        # search for path with flow reserve
        path, reserve = bfs_paths(graph, start, end)
        print(path)
        flow += reserve 
        '''for v, u in zip(path, path[1:]):
            if graph.has_edge(v, u):
                graph[v][u]['flow'] += reserve
            else:
                graph[u][v]['flow'] -= reserve'''
        for i in range(0,len(path)-1):
            graph[i][path[i+1]]["flow"] += flow
        
        print('flow increased by', reserve, 
          'at path', path,
          '; current flow', flow)


def bfs_paths(graph, start, goal):
    visited = []
    stack = []
    flow = 10000
    stack.append(start)
    while(stack):
        current = stack.pop(0)

        if (current not in visited):
            visited.append(current)
            
            for i in graph[current]:
                if(graph[current][i]['flow'] < graph[current][i]['capacity']):
                    
                    if(graph[current][i]['capacity'] < flow):
                        flow = graph[current][i]['capacity']
                    if(i == goal):
                        visited.append(i)
                        return visited, flow
                    if(i not in visited):
                        stack.append(i)
                else: 
                    
    return []


def depth_first_search(graph, source, sink):
    undirected = graph.to_undirected()
    explored = {source}
    stack = [(source, 0, dict(undirected[source]))]
    print(stack)
    
    while stack:
        v, _, neighbours = stack[-1]
        if v == sink:
            break
        
        # search the next neighbour
        while neighbours:
            u, e = neighbours.popitem()
            if u not in explored:
                break
        else:
            stack.pop()
            continue
        
        # current flow and capacity
        in_direction = graph.has_edge(v, u)
        capacity = e['capacity']
        flow = e['flow']
        neighbours = dict(undirected[u])

        # increase or redirect flow at the edge
        if in_direction and flow < capacity:
            stack.append((u, capacity - flow, neighbours))
            explored.add(u)
        elif not in_direction and flow:
            stack.append((u, flow, neighbours))
            explored.add(u)

    # (source, sink) path and its flow reserve
    reserve = min((f for _, f, _ in stack[1:]), default=0)
    path = [v for v, _, _ in stack]
    
    return path, reserve




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
print(lastNode)
search(graph, 0, lastNode)

