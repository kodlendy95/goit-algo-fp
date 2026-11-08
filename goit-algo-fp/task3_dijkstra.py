"""Завдання 3: алгоритм Дейкстри, пріоритетна черга на бінарній купі."""
from __future__ import annotations

import heapq
from math import inf

# Орієнтований граф: вершина -> список пар (сусід, вага).
Graph = dict[str, list[tuple[str, float]]]


def dijkstra(graph: Graph, start: str) -> tuple[dict[str, float], dict[str, str | None]]:
    """Повертає відстані й попередників. Ваги повинні бути невід'ємними."""
    vertices = set(graph)
    for neighbors in graph.values():
        for target, weight in neighbors:
            if weight < 0:
                raise ValueError('Алгоритм Дейкстри не підтримує від’ємні ваги.')
            vertices.add(target)
    if start not in vertices:
        raise ValueError(f'Початкова вершина {start!r} відсутня в графі.')

    distances = {vertex: inf for vertex in vertices}
    previous: dict[str, str | None] = {vertex: None for vertex in vertices}
    distances[start] = 0.0
    priority_queue: list[tuple[float, str]] = [(0.0, start)]
    while priority_queue:
        current_distance, vertex = heapq.heappop(priority_queue)
        if current_distance > distances[vertex]:
            continue  # Пропускаємо застарілий запис у купі.
        for neighbor, weight in graph.get(vertex, []):
            candidate = current_distance + weight
            if candidate < distances[neighbor]:
                distances[neighbor] = candidate
                previous[neighbor] = vertex
                heapq.heappush(priority_queue, (candidate, neighbor))
    return distances, previous


def reconstruct_path(previous: dict[str, str | None], start: str,
                     target: str) -> list[str]:
    """Відновлює шлях або повертає порожній список для недосяжної вершини."""
    if start not in previous or target not in previous:
        return []
    path = []
    current: str | None = target
    while current is not None:
        path.append(current)
        if current == start:
            return path[::-1]
        current = previous[current]
    return []


def sample_graph() -> Graph:
    return {
        'A': [('B', 4), ('C', 2)],
        'B': [('C', 1), ('D', 5)],
        'C': [('B', 1), ('D', 8), ('E', 10)],
        'D': [('E', 2), ('F', 6)],
        'E': [('F', 3)],
        'F': [],
        'G': [],  # Недосяжна вершина, відстань дорівнює inf.
    }


def main() -> None:
    start = 'A'
    distances, previous = dijkstra(sample_graph(), start)
    print(f'Найкоротші шляхи від вершини {start}:')
    for vertex in sorted(distances):
        distance = distances[vertex]
        if distance == inf:
            print(f'  {vertex}: недосяжна')
        else:
            route = ' → '.join(reconstruct_path(previous, start, vertex))
            print(f'  {vertex}: відстань {distance:g}, шлях {route}')


if __name__ == '__main__':
    main()
