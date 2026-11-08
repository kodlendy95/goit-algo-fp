"""Завдання 6: жадібний підхід та динамічне програмування (0/1 knapsack)."""
from __future__ import annotations

Items = dict[str, dict[str, int]]

items: Items = {
    'pizza': {'cost': 50, 'calories': 300},
    'hamburger': {'cost': 40, 'calories': 250},
    'hot-dog': {'cost': 30, 'calories': 200},
    'pepsi': {'cost': 10, 'calories': 100},
    'cola': {'cost': 15, 'calories': 220},
    'potato': {'cost': 25, 'calories': 350},
}


def validate(data: Items, budget: int) -> None:
    if not isinstance(budget, int) or budget < 0:
        raise ValueError('Бюджет має бути невід’ємним цілим числом.')
    if any(entry['cost'] <= 0 or entry['calories'] < 0 for entry in data.values()):
        raise ValueError('Ціна має бути додатною, калорійність — невід’ємною.')


def greedy_algorithm(data: Items, budget: int) -> tuple[list[str], int, int]:
    """Сортує за calories/cost; кожна страва може бути взята лише раз."""
    validate(data, budget)
    order = sorted(data, key=lambda name: data[name]['calories'] / data[name]['cost'],
                   reverse=True)
    selected, total_cost, total_calories = [], 0, 0
    for name in order:
        cost = data[name]['cost']
        if total_cost + cost <= budget:
            selected.append(name)
            total_cost += cost
            total_calories += data[name]['calories']
    return selected, total_cost, total_calories


def dynamic_programming(data: Items, budget: int) -> tuple[list[str], int, int]:
    """0/1 knapsack: оптимальний результат, час O(n×budget)."""
    validate(data, budget)
    names = list(data)
    n = len(names)
    dp = [[0] * (budget + 1) for _ in range(n + 1)]
    for i, name in enumerate(names, start=1):
        cost, calories = data[name]['cost'], data[name]['calories']
        for available in range(budget + 1):
            dp[i][available] = dp[i - 1][available]
            if cost <= available:
                candidate = dp[i - 1][available - cost] + calories
                if candidate > dp[i][available]:
                    dp[i][available] = candidate

    chosen = []
    remainder = budget
    for i in range(n, 0, -1):
        name = names[i - 1]
        if dp[i][remainder] != dp[i - 1][remainder]:
            chosen.append(name)
            remainder -= data[name]['cost']
    chosen.reverse()
    total_cost = sum(data[name]['cost'] for name in chosen)
    return chosen, total_cost, dp[n][budget]


def main() -> None:
    budget = 100
    print('Бюджет:', budget)
    for description, algorithm in [('Жадібний', greedy_algorithm),
                                   ('Динамічне програмування', dynamic_programming)]:
        names, cost, calories = algorithm(items, budget)
        print(f'{description}: {names}; вартість={cost}, калорії={calories}')


if __name__ == '__main__':
    main()
