# astar.py
import heapq

class Node:
    def __init__(self, name, neighbors=None):
        self.name = name
        self.neighbors = neighbors or []  # list of (Node, mode, cost, time)

def heuristic(a: Node, b: Node):
    return 0  # zero heuristic; override with great-circle if coords known

def astar(start: Node, goal: Node):
    open_set = [(0, start)]
    came_from = {}
    g_score = {start: 0}

    while open_set:
        _, current = heapq.heappop(open_set)
        if current == goal:
            path = [current]
            while current in came_from:
                current = came_from[current]
                path.append(current)
            return list(reversed(path))
        for neighbor, mode, cost, time in current.neighbors:
            tentative = g_score[current] + cost
            if tentative < g_score.get(neighbor, float("inf")):
                came_from[neighbor] = current
                g_score[neighbor] = tentative
                f_score = tentative + heuristic(neighbor, goal)
                heapq.heappush(open_set, (f_score, neighbor))
    return None
