#!/usr/bin/python
# -*- coding: utf-8 -*-


def solve_it(adj_list, node_count):
    # Modify this code to run your optimization algorithm

    # parse the input
    # build a trivial solution
    # every node has its own color
    solution = range(0, node_count)
    return solution

def prepare_output_data(solution):
    # prepare the solution in the specified output format
    output_data = str(len(solution)) + ' ' + '0' + '\n'
    output_data += ' '.join(map(str, solution))
    return output_data


import sys

class State:
    node_list = []
    color_count = 0
    def __init__(self, node_list, color_count):
        self. node_list = node_list
        self.color_count = color_count
    
    def is_feasible(self):
        for node in self.node_list:
            for adj in node.adj_list:
                if node.color != -1 and node.color == self.node_list[adj].color:
                    return False
        return True

    def __str__(self):
        return "Color Count: " + str(self.color_count) + "\n" + " Node State: " + str([str(node) for node in self.node_list])

class Node:
    id = -1
    adj_list = []
    color = -1
    degree = 0
    feasible_colors = {}
    def __init__(self, id, adj_list, feasible_colors, color = -1):
        self.id = id
        self.adj_list = adj_list
        self.feasible_colors = feasible_colors
        self.color = color

    def __str__(self):
        return "ID: " + str(self.id) + " Color: " + str(self.color) + " Adj: " + str(self.adj_list) + " Degree: " + str(self.degree)

def construct_init_state(node_count, edge_count, lines):

    node_list = [Node(i, [], {i, range(0, node_count)}, -1) for i in range(node_count)]
    for i in range(1, edge_count + 1):
        line = lines[i]
        parts = line.split()
        node_list[int(parts[0])].adj_list.append(int(parts[1]))
        node_list[int(parts[1])].adj_list.append(int(parts[0]))
        node_list[int(parts[0])].degree += 1
        node_list[int(parts[1])].degree += 1
    node_list.sort(key=lambda x: x.degree, reverse=True)
    state = State(node_list, 0)
    return state

def parse_input_data(file_location):
    print(file_location)
    with open(file_location, 'r') as input_data_file:
        input_data = input_data_file.read()
    lines = input_data.split('\n')

    first_line = lines[0].split()
    node_count = int(first_line[0])
    edge_count = int(first_line[1])
    adj_list = construct_init_state(node_count, edge_count, lines)
    return node_count, edge_count, adj_list

if __name__ == '__main__':
    import sys
    if len(sys.argv) > 1:
        print("hi")
        file_location = sys.argv[1].strip()
        print(file_location)
        node_count, edge_count, adj_list = parse_input_data(file_location)

        solution = solve_it(adj_list, node_count)
        solution = prepare_output_data(solution)
        print(solution)
    else:
        print('This test requires an input file.  Please select one from the data directory. (i.e. python solver.py ./data/gc_4_1)')

