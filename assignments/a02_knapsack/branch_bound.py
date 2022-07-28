
from assignments.a02_knapsack.schema import Item
from src.utils.log_config import get_logger

logger = get_logger(__name__, level="DEBUG")


def depth_first(items: list[Item], capacity: int):
    ranked = rank_by_density(items)
    best_value, best_weight, taken = relaxed_integer(ranked, capacity)
    logger.info(f"Best possible value with int->float relaxion: value={best_value}, weight={best_weight}")
    return ranked


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
            taken.append((frac_to_take, itm))
            break
        
    return best_value, best_weight, taken


