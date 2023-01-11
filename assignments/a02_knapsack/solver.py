#!/usr/bin/python
# -*- coding: utf-8 -*-

from pprint import pformat
from typing import List, Tuple

from assignments.a02_knapsack.branch_bound import depth_first
from assignments.a02_knapsack.schema import Item
from src.utils.directory import DIR
from src.utils.log_config import get_logger

DATA_DIR = DIR.ASSIGN.KNAPSACK_02 / "data"

logger = get_logger(__name__)



def solve_it(input_data):

    # parse file into useable data
    capacity, items = parse_input(input_data)
    logger.info(f"Max Capacity: {capacity}\nItems:\n{pformat(items)}")

    # run an algorithm to solve the problem, key work goes into this function
    ranked = depth_first(items, capacity)
    logger.info(f"Ranked items:\n{pformat(ranked)}")

    value, taken = organise_results(ranked, items)
    
    # prepare the solution in the specified output format
    output_data = format_result(value, taken)
    return output_data


def organise_results(ranked: List[Item], items: List[Item]) -> Tuple[int, list]:
    """Turn list of chosen items back into format required for results"""
    value = sum([i.value for i in ranked])
    indices = {i.idx for i in ranked}
    taken = [1 if i in indices else 0 for i in range(1, len(items)+1)]
    return value, taken


def parse_input(input_data):
    # parse the input
    lines = input_data.split('\n')

    firstLine = lines[0].split()
    item_count = int(firstLine[0])
    capacity = int(firstLine[1])

    items = []

    for i, line in enumerate(lines[1:-1]):
        itm_value, itm_weight = map(int, line.split())
        items.append(Item(i+1, itm_value, itm_weight))
    return capacity, items


def format_result(value, taken):
    output_data = str(value) + ' ' + str(0) + '\n'
    output_data += ' '.join(map(str, taken))
    return output_data


if __name__ == '__main__':
    import sys
    if len(sys.argv) > 1:
        file_location = sys.argv[1].strip()
        filename = file_location.split('/')[-1]
        file_location = DATA_DIR / filename
        
    else:
        logger.info("Using default input file ks_4_0")
        file_location = DATA_DIR / "ks_4_0"
        filename = file_location.stem

    with open(file_location, 'r') as input_data_file:
        input_data = input_data_file.read()
    
    print(f"Result for {filename} =\n", solve_it(input_data))


