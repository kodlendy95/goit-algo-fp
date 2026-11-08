"""Завдання 4: перетворення масиву бінарної купи на дерево та візуалізація."""
from __future__ import annotations

import argparse
import heapq

from tree_utils import Node, draw_tree


def heap_to_tree(heap: list[int]) -> Node | None:
    """Індекс вузла i: лівий на 2i+1, правий на 2i+2."""
    if not heap:
        return None
    nodes = [Node(value) for value in heap]
    for index, parent in enumerate(nodes):
        left = 2 * index + 1
        right = 2 * index + 2
        if left < len(nodes):
            parent.left = nodes[left]
        if right < len(nodes):
            parent.right = nodes[right]
    return nodes[0]


def main() -> None:
    parser = argparse.ArgumentParser(description='Візуалізація мін-купи')
    parser.add_argument('--save', help='Файл PNG')
    parser.add_argument('--no-show', action='store_true')
    args = parser.parse_args()
    data = [14, 4, 9, 1, 7, 3, 12, 8, 6, 5]
    heapq.heapify(data)  # heapq побудований на бінарній мін-купі.
    root = heap_to_tree(data)
    print('Мін-купа (масив):', data)
    if root is not None:
        draw_tree(root, 'Бінарна мін-купа', save_path=args.save,
                  show=not args.no_show)


if __name__ == '__main__':
    main()
