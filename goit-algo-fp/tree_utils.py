"""Спільні функції побудови і візуалізації бінарних дерев для завдань 4–5."""
from __future__ import annotations

import uuid
from collections import deque
from pathlib import Path

import matplotlib.pyplot as plt
import networkx as nx


class Node:
    def __init__(self, key: int, color: str = '#9ed6ef') -> None:
        self.left: Node | None = None
        self.right: Node | None = None
        self.val = key
        self.color = color
        self.id = str(uuid.uuid4())


def add_edges(graph: nx.DiGraph, node: Node, pos: dict[str, tuple[float, float]],
              x: float = 0, y: float = 0, layer: int = 1) -> nx.DiGraph:
    """Створює граф дерева і координати вузлів. Без рекурсії."""
    queue = deque([(node, x, y, layer)])
    while queue:
        current, current_x, current_y, current_layer = queue.popleft()
        graph.add_node(current.id, color=current.color, label=current.val)
        for child, direction in ((current.left, -1), (current.right, 1)):
            if child is None:
                continue
            child_x = current_x + direction / (2 ** current_layer)
            child_y = current_y - 1
            graph.add_edge(current.id, child.id)
            pos[child.id] = (child_x, child_y)
            queue.append((child, child_x, child_y, current_layer + 1))
    return graph


def draw_tree(root: Node, title: str = 'Бінарне дерево',
              save_path: str | None = None, show: bool = True,
              ax: plt.Axes | None = None) -> plt.Figure:
    tree = nx.DiGraph()
    pos = {root.id: (0.0, 0.0)}
    add_edges(tree, root, pos)
    colors = [data['color'] for _, data in tree.nodes(data=True)]
    labels = {identifier: data['label'] for identifier, data in tree.nodes(data=True)}
    if ax is None:
        fig, ax = plt.subplots(figsize=(9, 6))
    else:
        fig = ax.figure
    ax.clear()
    nx.draw(tree, pos=pos, labels=labels, arrows=False,
            node_size=1800, node_color=colors, edgecolors='#274263',
            linewidths=1.3, font_size=11, font_weight='bold', ax=ax)
    ax.set_title(title, fontsize=13)
    if save_path:
        Path(save_path).parent.mkdir(parents=True, exist_ok=True)
        fig.savefig(save_path, dpi=180, bbox_inches='tight')
    if show:
        plt.show()
    return fig
