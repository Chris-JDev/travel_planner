# utils.py
import itertools

def solve_tsp_bruteforce(distance_matrix: list[list[int]], start_index: int = 0):
    n = len(distance_matrix)
    indices = list(range(n))
    best_order, best_cost = None, float("inf")

    # fix the first city to be `start_index`
    others = [i for i in indices if i != start_index]
    for perm in itertools.permutations(others):
        order = [start_index] + list(perm)
        cost = sum(
            distance_matrix[order[i]][order[i+1]]
            for i in range(len(order)-1)
        )
        if cost < best_cost:
            best_cost = cost
            best_order = order

    return best_order, best_cost
