import dataclasses as dc

import pandas as pd

from assignments.a02_knapsack.schema import Item
from src.utils.log_config import get_logger

logger = get_logger(__name__, level="DEBUG")


def depth_first(items: list[Item], capacity: int):
    ranked = rank_by_density(items)
    best_value, best_weight, taken = relaxed_integer(ranked, capacity)
    logger.info(f"Best possible value with int->float relaxation: value={best_value}, weight={best_weight}")
    
    df = pd.DataFrame(list(map(dc.asdict, items)))
    df = df.sort_values('density', ascending=False).reset_index(drop=True)

    best_choices = [False] * len(df)  # start with nothing chosen
    remaining_weight = capacity

    for i, (itm_val, itm_wgt) in df[['value', 'weight']].iterrows():
        best_choices[i] = True

        weight_if_chosen = df.loc[best_choices, 'weight'].sum()
        value_if_chosen = df.loc[best_choices, 'value'].sum()

        if weight_if_chosen > capacity:
            logger.debug(f"Item {i} /{itm_wgt} is too heavy, skipping")
            best_choices[i] = False
        else:
            remaining_weight = capacity - weight_if_chosen
            logger.debug(f"Remaining weight: {remaining_weight}")

        logger.info(f"current:\n{df.loc[best_choices,:]}")





    return [Item(**r) for r in df.loc[best_choices,['idx', 'value', 'weight']].to_dict('records')]


def rank_by_density(items: list[Item]) -> list[Item]:
    return sorted(items, key=lambda item: item.density, reverse=True)


def relaxed_integer(items: list[Item], capacity: int) -> int:
    i, best_weight, best_value = 0, 0, 0
    taken = []
    while best_weight <= capacity:
        itm = items[i]
        if best_weight + itm.weight <= capacity:
            logger.debug(f"Adding item {itm}")
            taken.append(itm)
            best_weight += itm.weight
            best_value += itm.value
            i += 1
        else:
            remaining_weight = capacity - best_weight
            frac_to_take = remaining_weight / itm.weight
            logger.debug(f"Can only take {round(frac_to_take, 2)} fraction of item {itm}")
            best_weight += frac_to_take * itm.weight
            best_value += frac_to_take * itm.value
            taken.append(itm)
            break
        
    return best_value, best_weight, taken


