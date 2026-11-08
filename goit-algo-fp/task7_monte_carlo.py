"""Завдання 7: суми двох кубиків, Монте-Карло та точна аналітика."""
from __future__ import annotations

import argparse
import random
from collections import Counter
from pathlib import Path

import matplotlib.pyplot as plt


def simulate_dice(throws: int = 200_000, seed: int | None = 42) -> dict[int, float]:
    if not isinstance(throws, int) or throws <= 0:
        raise ValueError('Кількість кидків має бути додатним цілим числом.')
    random_generator = random.Random(seed)
    counts = Counter(random_generator.randint(1, 6) + random_generator.randint(1, 6)
                     for _ in range(throws))
    return {value: counts[value] / throws for value in range(2, 13)}


def analytical_probabilities() -> dict[int, float]:
    """Кількість можливих пар для суми s: 6 - abs(7-s), всього 36 пар."""
    return {value: (6 - abs(7 - value)) / 36 for value in range(2, 13)}


def draw_comparison(empirical: dict[int, float], save_path: str | None = None,
                    show: bool = True) -> plt.Figure:
    analytical = analytical_probabilities()
    values = list(range(2, 13))
    positions = list(range(len(values)))
    fig, ax = plt.subplots(figsize=(11, 6))
    bar_width = 0.39
    ax.bar([x - bar_width / 2 for x in positions],
           [empirical[s] * 100 for s in values], bar_width, label='Монте-Карло')
    ax.bar([x + bar_width / 2 for x in positions],
           [analytical[s] * 100 for s in values], bar_width, label='Аналітична')
    ax.set_xticks(positions, [str(x) for x in values])
    ax.set_xlabel('Сума двох кубиків')
    ax.set_ylabel('Імовірність, %')
    ax.set_title('Метод Монте-Карло: порівняння з теорією')
    ax.grid(axis='y', alpha=0.2)
    ax.legend()
    fig.tight_layout()
    if save_path:
        Path(save_path).parent.mkdir(parents=True, exist_ok=True)
        fig.savefig(save_path, dpi=180, bbox_inches='tight')
    if show:
        plt.show()
    return fig


def main() -> None:
    parser = argparse.ArgumentParser(description='Монте-Карло для двох кубиків')
    parser.add_argument('--throws', type=int, default=200_000)
    parser.add_argument('--seed', type=int, default=42)
    parser.add_argument('--save', help='Файл PNG з графіком')
    parser.add_argument('--no-show', action='store_true')
    args = parser.parse_args()
    empirical = simulate_dice(args.throws, args.seed)
    analytical = analytical_probabilities()
    print(f'Кількість кидків: {args.throws}; seed={args.seed}')
    print('Сума | Монте-Карло | Теоретична | Відхилення, в.п.')
    for value in range(2, 13):
        observed, expected = empirical[value] * 100, analytical[value] * 100
        print(f'{value:>4} | {observed:>10.3f}% | {expected:>9.3f}% | {abs(observed-expected):>9.3f}')
    deviation = max(abs(empirical[s] - analytical[s]) for s in range(2, 13)) * 100
    print(f'Максимальне абсолютне відхилення: {deviation:.3f} відсоткового пункту')
    figure = draw_comparison(empirical, save_path=args.save, show=not args.no_show)
    plt.close(figure)


if __name__ == '__main__':
    main()
