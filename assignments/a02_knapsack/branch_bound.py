import dataclasses as dc

import numpy as np
import pandas as pd

from assignments.a02_knapsack.schema import Item
from src.utils.log_config import get_logger, VERBOSE

logger = get_logger(__name__, level="VERBOSE")

"""
    each tree node is a an assessment of the scenario if the current single item in question is taken or not

    at each node, we need to ask 'if we decide to keep/take item X, considering the prior history further up the tree':
    - can we fit it in the knapsack? if not, it's infeasible, stop
    - what is the current value of the knapsack?
    - what is the best possible total value at the end of the tree if we decide to/not take this item?
       if this best possible value is less than the best actual value we've found so far, stop
    -> otherwise, take the item and continue down the tree

    """

def depth_first(items: list[Item], capacity: int):
    ranked = rank_by_density(items)
    # first just find best possible solution if we ignore integer constraints
    best_value, best_weight, taken = relaxed_integer(ranked, capacity)
    logger.info(f"Best possible value with int->float relaxation: value={best_value}, weight={best_weight}; {len(taken)} items of indexes={sorted([i.idx for i in taken])}")
    
    df = pd.DataFrame(list(map(dc.asdict, ranked)))

    mask_choices = [False] * len(df)  # start with nothing chosen
    remaining_weight = capacity  # gets whittled down as we loop through
    best_estimate = 0  # gets improved as we loop through

    for i, (idx, itm_val, itm_wgt) in df[['idx', 'value', 'weight']].iterrows():
        mask_choices = downwards_traverse(capacity, df, mask_choices, remaining_weight, best_estimate)
        # remaining_estimate = relaxed_integer()
        print(mask_choices)

    return [Item(**r) for r in df.loc[mask_choices,['idx', 'value', 'weight']].to_dict('records')]


def downwards_traverse(capacity, df, mask_choices, remaining_weight, best_estimate):

    for i, (idx, itm_val, itm_wgt) in df[['idx', 'value', 'weight']].iterrows():
        mask_choices[i] = True  # temporarily choose this item

        weight_if_chosen, value_if_chosen = df.loc[mask_choices, ['value', 'weight']].sum()

        # best_remaining_value = 

        if weight_if_chosen > capacity:
            logger.debug(f"Skipping item {i} / wgt={itm_wgt}, heavier than remaining {remaining_weight}")
            mask_choices[i] = False  # reset to not choose this item

        elif value_if_chosen < best_estimate:
            logger.debug(f"Skipping item {i} / val={itm_val} is too cheap, skipping")
            mask_choices[i] = False
        else:
            remaining_weight = capacity - weight_if_chosen
            logger.debug(f"Item {idx} added. Remaining weight: {remaining_weight}")

    logger.debug(f"current:\n{df.loc[mask_choices,:]}")
    
    return mask_choices


def rank_by_density(items: list[Item]) -> list[Item]:
    # TODO should we also rank by weight for items where density is identical? Take smallest?
    return np.array(sorted(items, key=lambda item: item.density, reverse=True))


def relaxed_integer(items: list[Item], capacity: int, chosen_weight: float = 0, chosen_value: float = 0) -> int:
    i, taken = 0, []
    if chosen_weight or chosen_value:
        logger.log(VERBOSE, f"chosen weight={chosen_weight}, chosen value={chosen_value}")
    while chosen_weight <= capacity:
        itm = items[i]
        if chosen_weight + itm.weight <= capacity:
            logger.debug(f"Adding item {itm} to best case selection")
            taken.append(itm)
            chosen_weight += itm.weight
            chosen_value += itm.value
            logger.log(VERBOSE, f"chosen weight={chosen_weight}, chosen value={chosen_value}")
            i += 1
        else:
            remaining_weight = capacity - chosen_weight
            frac_to_take = remaining_weight / itm.weight
            logger.debug(f"Can only take {round(frac_to_take, 2)} fraction of item {itm} as final addition to best case selection")
            chosen_weight += frac_to_take * itm.weight
            chosen_value += frac_to_take * itm.value
            taken.append(itm)
            break
        
    return chosen_value, chosen_weight, taken


