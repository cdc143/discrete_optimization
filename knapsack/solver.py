#!/usr/bin/python
# -*- coding: utf-8 -*-

from collections import namedtuple
import numpy as np
from collections import deque

Item = namedtuple("Item", ['index', 'value', 'weight', 'density'])
class Knapsack:
    capacity = 0
    def __init__(self, capacity):
        self.capacity = capacity
class Node:
    level = 0
    value = 0
    capacity = 0
    estimated_value = 0
    contains = np.zeros(1).astype(int)
    def __init__(self, level, value, capacity, estimated_value, contains):
        self.level = level
        self.value = value
        self.capacity = capacity
        self.estimated_value = estimated_value
        self.contains = contains

def parse_input_file(input_data):
    lines = input_data.split('\n')
    firstLine = lines[0].split()
    item_count = int(firstLine[0])
    capacity = int(firstLine[1])
    k = Knapsack(capacity)
    items = []
    for i in range(1, item_count+1):
        line = lines[i]
        parts = line.split()
        items.append(Item(i-1, int(parts[0]), int(parts[1]), float(parts[0]) / float(parts[1])))
    return (k, items)

def prepare_output(value, taken, optimal = 0):
    output_data = str(value) + ' ' + str(optimal) + '\n'
    output_data += ' '.join(map(str, taken))
    return output_data

def determine_solution_greedy(k, items):
    optimal = 0
    value = 0
    weight = 0
    taken = [0]*len(items)

    for item in items:
        if weight + item.weight <= k.capacity:
            taken[item.index] = 1
            value += item.value
            weight += item.weight
    return (value, taken, optimal)

def determine_solution_bnb(k, items):
    optimal = 1
    bound = determine_inital_bound(k.capacity, items)
    best_value = -1
    best_taken = np.zeros(len(items), dtype=int)
    stack = deque()
    root = Node(0, 0, k.capacity, bound, np.zeros(len(items), dtype=int))
    stack.appendleft(root)
    while stack:
        node = stack.popleft()
        if node.level >= len(items):
            continue
        # If the node is not promising, skip it
        if node.estimated_value < best_value:
            continue
        item = items[node.level]

        # Don't take the item (right subtree)
        pass_est = node.value + node.capacity * item.density
        stack.appendleft(Node(node.level + 1, node.value, node.capacity, pass_est, np.copy(node.contains)))

        # Take the item (left subtree)
        if node.capacity >=  item.weight:
            node.contains[item.index] = 1
            best_value = max(best_value, node.value + item.value)
            if best_value == node.value + item.value:
                best_taken = np.copy(node.contains)
            stack.appendleft(Node(node.level+1, node.value + item.value, node.capacity - item.weight, node.estimated_value, np.copy(node.contains)))
    return (best_value, best_taken, optimal)

def determine_inital_bound(capacity, items):
    value = 0
    weight = 0

    # Take as many 'full' items as possible in order of density
    for item in items:
        if weight + item.weight <= capacity:
            value += item.value
            weight += item.weight
        # Now take a fraction of the next item
        else:
            frac = item.density * (capacity - weight)
            weight += frac * item.weight
            value += frac * item.value
            break
    return value

def solve_it_dp(count, capacity, items):

    value = 0
    weight = 0
    taken = [0] * count
    optimal = 1

    #Base table of zeros
    arr = np.zeros((capacity + 1, count + 1))

    bundle_weight = 0
    #Fill in the table
    for i in range(1, count + 1):
        for j in range(1, capacity + 1):
            cur_v = items[i - 1].value
            cur_w = items[i - 1].weight
            prev_bundle_weight = max(0, j - items[i - 1].weight)
            prev_bundle_val = arr[j - items[i - 1].weight, i - 1]

            #We can fit the current item in the knapsack
            #We thus choose between the current item and
            #the previous one
            if j >= prev_bundle_weight + cur_w:
                old_val = arr[j, i - 1]
                new_val = prev_bundle_val + cur_v
                arr[j,i] = max(old_val, new_val)
            #We can't fit the current item
            #take the old bundle value
            else:
                arr[j, i] = arr[j, i - 1]

    #Compute the trace
    i, j = capacity, count
    value = arr[i, j]
    while (j != 0):
        #We did not take the j-th item
        if arr[i, j] == arr[i, j - 1]:
            taken[j - 1] = 0
        #We took the j-th item
        else:
            taken[j - 1] = 1
            weight += items[j - 1].weight
            i -= items[j - 1].weight
        j -= 1



    return (int(value), int(weight), taken, optimal)


def solve_it(input_data):
    # Modify this code to run your optimization algorithm

    # parse the input
    (k, items) = parse_input_file(input_data)

    # sort items by density in descending order
    sorted_items = sorted(items, key=lambda x: x[-1], reverse=True)
    # depth first branch and bound algorithm, using greedy initial bound
    value, taken, optimal = determine_solution_bnb(k, sorted_items)

    # naive greedy algorithm, take items in items in order until knapsack is full
    #value, taken, optimal = determine_solution_greedy(k, items)

    # solve knapsack problem using dynamic programming
    #value, weight, taken, optimal = solve_it_dp(len(items), k.capacity, items)
    
    # prepare the solution in the specified output format
    output_data = prepare_output(value, taken, optimal)
    return output_data


if __name__ == '__main__':
    import sys
    if len(sys.argv) > 1:
        file_location = sys.argv[1].strip()
        with open(file_location, 'r') as input_data_file:
            input_data = input_data_file.read()
        print(solve_it(input_data))
    else:
        print('This test requires an input file.  Please select one from the data directory. (i.e. python solver.py ./data/ks_4_0)')

