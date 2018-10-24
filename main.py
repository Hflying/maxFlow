from graphviz import Source


class Edge:
    start = -1
    end = -1
    flow = 0

    def __init__(self, start, end, value):
        self.start = start
        self.end = end
        self.flow = value

class Node:
    name = -1
    edges = []

    def __init__(self, name, edge):
        self.name = name
        self.edges.append(edge)

    def add(self, value, end):
        self.edges.append()


def search(index, nodes, lastNode, path):
        if index == lastNode:
            return path
        



edges = []
lastNode = 0
nodes = []
with open("train.txt") as f:
    lines = f.readlines()
    for line in lines:
        if "digraph {" not in line and "}" not in line:
            print(line)
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
            

            print(fname)
            print(sname)
            print(value)

            if(int(fname) > lastNode):
                lastNode = int(fname)
            if(int(sname) > lastNode):
                lastNode = int(sname)
            edge = Edge(int(fname), int(sname), int(value))
            nodes.append(Node(int(fname), edge))
