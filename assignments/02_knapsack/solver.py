#!/usr/bin/python
# -*- coding: utf-8 -*-

from collections import namedtuple
from pprint import pformat

from src.utils.log_config import get_logger

logger = get_logger(__name__)

Item = namedtuple("Item", ['index', 'value', 'weight'])

def solve_it(input_data):

    # parse file into useable data
    capacity, items = parse_input(input_data)
    logger.info(f"Items:\n{pformat(items)}")

    # run an algorithm to solve the problem, key work goes into this function
    value, taken = solve_problem(capacity, items)
    
    # prepare the solution in the specified output format
    output_data = format_result(value, taken)
    return output_data


def solve_problem(capacity, items):
    # a trivial algorithm for filling the knapsack
    # it takes items in-order until the knapsack is full
    value = 0
    weight = 0
    taken = [0]*len(items)

    for item in items:
        if weight + item.weight <= capacity:
            taken[item.index] = 1
            value += item.value
            weight += item.weight

    return value, taken


def parse_input(input_data):
    # parse the input
    lines = input_data.split('\n')

    firstLine = lines[0].split()
    item_count = int(firstLine[0])
    capacity = int(firstLine[1])

    items = []

    for i in range(1, item_count+1):
        line = lines[i]
        parts = line.split()
        items.append(Item(i-1, int(parts[0]), int(parts[1])))
    return capacity, items


def format_result(value, taken):
    output_data = str(value) + ' ' + str(0) + '\n'
    output_data += ' '.join(map(str, taken))
    return output_data


if __name__ == '__main__':
    import sys
    if len(sys.argv) > 1:
        file_location = sys.argv[1].strip()
        with open(file_location, 'r') as input_data_file:
            input_data = input_data_file.read()
        filename = file_location.split('/')[-1]
        print(f"Result for {filename} =\n", solve_it(input_data))
    else:
        print('This test requires an input file.  Please select one from the data directory. (i.e. python solver.py ./data/ks_4_0)')

