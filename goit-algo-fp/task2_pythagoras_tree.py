"""Завдання 2: рекурсивний фрактал «дерево Піфагора» зі справжніх квадратів."""
from __future__ import annotations

import argparse
from pathlib import Path

import matplotlib.pyplot as plt
from matplotlib.patches import Polygon

Point = tuple[float, float]


def add(a: Point, b: Point) -> Point:
    return (a[0] + b[0], a[1] + b[1])


def rotate90(v: Point) -> Point:
    return (-v[1], v[0])


def draw_pythagoras_tree(depth: int, save_path: str | None = None,
                         show: bool = True) -> plt.Figure:
    """Малює квадрат і два дочірні квадрати, повернуті на 45 градусів."""
    if not isinstance(depth, int) or not 0 <= depth <= 12:
        raise ValueError('Рівень рекурсії має бути цілим числом від 0 до 12.')

    fig, ax = plt.subplots(figsize=(10, 8))
    min_x = min_y = float('inf')
    max_x = max_y = float('-inf')
    palette = plt.get_cmap('YlGn')

    def square(origin: Point, side: Point, level: int) -> None:
        nonlocal min_x, max_x, min_y, max_y
        vertical = rotate90(side)
        top_left = add(origin, vertical)
        top_right = add(top_left, side)
        bottom_right = add(origin, side)
        corners = [origin, bottom_right, top_right, top_left]
        for x, y in corners:
            min_x, max_x = min(min_x, x), max(max_x, x)
            min_y, max_y = min(min_y, y), max(max_y, y)

        color = palette(0.35 + 0.6 * (depth - level) / max(depth, 1))
        ax.add_patch(Polygon(corners, closed=True, facecolor=color,
                             edgecolor='#234c2c', linewidth=0.35))
        if level == 0:
            return
        # Кожен дочірній квадрат має сторону 1/sqrt(2) від батьківського.
        left_side = ((side[0] + vertical[0]) / 2,
                     (side[1] + vertical[1]) / 2)
        right_side = ((side[0] - vertical[0]) / 2,
                      (side[1] - vertical[1]) / 2)
        apex = add(top_left, left_side)
        square(top_left, left_side, level - 1)
        square(apex, right_side, level - 1)

    square((0.0, 0.0), (1.0, 0.0), depth)
    margin = max(max_x - min_x, max_y - min_y) * 0.05 + 0.02
    ax.set_xlim(min_x - margin, max_x + margin)
    ax.set_ylim(min_y - margin, max_y + margin)
    ax.set_aspect('equal', adjustable='box')
    ax.axis('off')
    ax.set_title(f'Дерево Піфагора — рівень рекурсії {depth}')
    fig.tight_layout()
    if save_path:
        Path(save_path).parent.mkdir(parents=True, exist_ok=True)
        fig.savefig(save_path, dpi=180, bbox_inches='tight')
    if show:
        plt.show()
    return fig


def main() -> None:
    parser = argparse.ArgumentParser(description='Побудова дерева Піфагора')
    parser.add_argument('--depth', type=int, help='Рівень рекурсії від 0 до 12')
    parser.add_argument('--save', help='Зберегти результат у PNG')
    parser.add_argument('--no-show', action='store_true', help='Не відкривати вікно')
    args = parser.parse_args()
    if args.depth is None:
        args.depth = int(input('Введіть рівень рекурсії (0–12): '))
    draw_pythagoras_tree(args.depth, save_path=args.save, show=not args.no_show)


if __name__ == '__main__':
    main()
