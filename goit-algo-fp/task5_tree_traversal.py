"""Завдання 5: ітеративні DFS (стек) та BFS (черга), колір і GIF по кроках."""
from __future__ import annotations

import argparse
from collections import deque
from pathlib import Path

import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation, PillowWriter

from tree_utils import Node, draw_tree

UNVISITED = '#E5E7EB'
DARK = (11, 48, 106)
LIGHT = (176, 224, 250)


def sample_tree() -> Node:
    root = Node(0)
    root.left = Node(4)
    root.left.left = Node(5)
    root.left.right = Node(10)
    root.right = Node(1)
    root.right.left = Node(3)
    return root


def dfs(root: Node | None) -> list[Node]:
    """Depth-first, preorder: стек; рекурсія не застосовується."""
    if root is None:
        return []
    stack = [root]
    visited = []
    while stack:
        node = stack.pop()
        visited.append(node)
        if node.right is not None:
            stack.append(node.right)
        if node.left is not None:
            stack.append(node.left)
    return visited


def bfs(root: Node | None) -> list[Node]:
    """Breadth-first: черга deque; рекурсія не застосовується."""
    if root is None:
        return []
    queue = deque([root])
    visited = []
    while queue:
        node = queue.popleft()
        visited.append(node)
        if node.left is not None:
            queue.append(node.left)
        if node.right is not None:
            queue.append(node.right)
    return visited


def gradient_colors(count: int) -> list[str]:
    """Унікальні RGB-кольори #RRGGBB від темного до світлого."""
    if count <= 0:
        return []
    result = []
    for index in range(count):
        progress = index / max(count - 1, 1)
        rgb = tuple(round(a + (b - a) * progress)
                    for a, b in zip(DARK, LIGHT))
        result.append('#' + ''.join(f'{channel:02X}' for channel in rgb))
    return result


def set_step_colors(root: Node, order: list[Node], step: int) -> None:
    """Фарбує перші step вузлів; ще не відвідані — сірі."""
    for node in bfs(root):
        node.color = UNVISITED
    for node, color in zip(order[:step], gradient_colors(len(order))):
        node.color = color


def save_animation(root: Node, order: list[Node], name: str, path: str) -> None:
    """Кожен кадр GIF показує наступний відвіданий вузол."""
    fig, ax = plt.subplots(figsize=(9, 6))

    def update(step: int) -> None:
        set_step_colors(root, order, step)
        draw_tree(root, f'{name}: крок {step}/{len(order)}', show=False, ax=ax)

    animation = FuncAnimation(fig, update, frames=range(len(order) + 1),
                              interval=750, repeat=False)
    Path(path).parent.mkdir(parents=True, exist_ok=True)
    animation.save(path, writer=PillowWriter(fps=1.3))
    plt.close(fig)


def main() -> None:
    parser = argparse.ArgumentParser(description='Обходи дерева DFS і BFS')
    parser.add_argument('--save-dir', default=None, help='Папка для PNG')
    parser.add_argument('--animate', action='store_true', help='Створити покрокові GIF')
    parser.add_argument('--no-show', action='store_true')
    args = parser.parse_args()

    root = sample_tree()
    algorithms = [('DFS (стек)', 'dfs', dfs(root)),
                  ('BFS (черга)', 'bfs', bfs(root))]
    for title, short_name, order in algorithms:
        print(f'{title}:', [node.val for node in order])
        if args.save_dir and args.animate:
            save_animation(root, order, title, str(Path(args.save_dir) / f'task5_{short_name}.gif'))
        set_step_colors(root, order, len(order))
        file_path = str(Path(args.save_dir) / f'task5_{short_name}.png') if args.save_dir else None
        figure = draw_tree(root, f'{title}: порядок обходу (темний → світлий)',
                           save_path=file_path, show=not args.no_show)
        plt.close(figure)


if __name__ == '__main__':
    main()
