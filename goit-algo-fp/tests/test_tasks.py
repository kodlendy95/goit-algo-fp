"""Запуск: python -m unittest discover -s tests -v"""
import itertools
import unittest
from math import inf

from task1_linked_list import LinkedList, merge_sorted_lists
from task2_pythagoras_tree import draw_pythagoras_tree
from task3_dijkstra import dijkstra, reconstruct_path, sample_graph
from task4_heap_visualization import heap_to_tree
from task5_tree_traversal import bfs, dfs, gradient_colors, sample_tree
from task6_food_optimization import (dynamic_programming, greedy_algorithm, items)
from task7_monte_carlo import analytical_probabilities, simulate_dice


class TestTask1(unittest.TestCase):
    def test_reverse_sort_merge(self):
        first = LinkedList([4, 2, 7, 1, 5, 3])
        original_ids = set()
        node = first.head
        while node:
            original_ids.add(id(node))
            node = node.next
        first.reverse()
        self.assertEqual(first.to_list(), [3, 5, 1, 7, 2, 4])
        first.insertion_sort()
        self.assertEqual(first.to_list(), [1, 2, 3, 4, 5, 7])
        self.assertEqual(id(first.tail), id(first.head.next.next.next.next.next))
        current_ids = set()
        node = first.head
        while node:
            current_ids.add(id(node))
            node = node.next
        self.assertEqual(original_ids, current_ids)
        second = LinkedList([0, 2, 6, 8])
        result = merge_sorted_lists(first, second)
        self.assertEqual(result.to_list(), [0, 1, 2, 2, 3, 4, 5, 6, 7, 8])
        self.assertEqual(first.to_list(), [1, 2, 3, 4, 5, 7])
        self.assertEqual(merge_sorted_lists(LinkedList(), second).to_list(), [0, 2, 6, 8])
        empty = LinkedList()
        empty.reverse()
        empty.insertion_sort()
        self.assertEqual(empty.to_list(), [])


class TestTask2(unittest.TestCase):
    def test_depth_zero(self):
        import matplotlib.pyplot as plt
        fig = draw_pythagoras_tree(0, show=False)
        self.assertEqual(len(fig.axes[0].patches), 1)
        plt.close(fig)
        fig = draw_pythagoras_tree(3, show=False)
        self.assertEqual(len(fig.axes[0].patches), 2**4 - 1)
        plt.close(fig)


class TestTask3(unittest.TestCase):
    def test_shortest_path(self):
        distances, prev = dijkstra(sample_graph(), 'A')
        self.assertEqual(distances['A'], 0)
        self.assertEqual(distances['B'], 3)
        self.assertEqual(distances['D'], 8)
        self.assertEqual(distances['E'], 10)
        self.assertEqual(distances['F'], 13)
        self.assertEqual(distances['G'], inf)
        self.assertEqual(reconstruct_path(prev, 'A', 'F'), ['A', 'C', 'B', 'D', 'E', 'F'])
        self.assertEqual(reconstruct_path(prev, 'A', 'G'), [])

    def test_invalid_weight(self):
        with self.assertRaises(ValueError):
            dijkstra({'A': [('B', -1)]}, 'A')


class TestTask4(unittest.TestCase):
    def test_heap_tree_positions(self):
        root = heap_to_tree([1, 3, 2, 8, 9])
        self.assertIsNotNone(root)
        self.assertEqual(root.val, 1)
        self.assertEqual(root.left.val, 3)
        self.assertEqual(root.right.val, 2)
        self.assertEqual(root.left.left.val, 8)
        self.assertIsNone(heap_to_tree([]))


class TestTask5(unittest.TestCase):
    def test_traversals(self):
        root = sample_tree()
        self.assertEqual([node.val for node in dfs(root)], [0, 4, 5, 10, 1, 3])
        self.assertEqual([node.val for node in bfs(root)], [0, 4, 1, 5, 10, 3])
        self.assertEqual(len(set(gradient_colors(6))), 6)
        self.assertTrue(all(len(c) == 7 and c.startswith('#') for c in gradient_colors(6)))
        self.assertEqual(dfs(None), [])
        self.assertEqual(bfs(None), [])


class TestTask6(unittest.TestCase):
    def test_results(self):
        greedy = greedy_algorithm(items, 100)
        dynamic = dynamic_programming(items, 100)
        self.assertLessEqual(greedy[1], 100)
        self.assertLessEqual(dynamic[1], 100)
        self.assertEqual(dynamic[2], 970)
        self.assertGreaterEqual(dynamic[2], greedy[2])
        self.assertEqual(dynamic_programming(items, 0), ([], 0, 0))

    def test_dp_brute_force(self):
        keys = list(items)
        for budget in range(0, 121, 5):
            optimal = 0
            for count in range(len(keys) + 1):
                for combo in itertools.combinations(keys, count):
                    cost = sum(items[x]['cost'] for x in combo)
                    if cost <= budget:
                        optimal = max(optimal, sum(items[x]['calories'] for x in combo))
            self.assertEqual(dynamic_programming(items, budget)[2], optimal)


class TestTask7(unittest.TestCase):
    def test_probabilities(self):
        theory = analytical_probabilities()
        observed = simulate_dice(100_000, seed=42)
        self.assertAlmostEqual(sum(theory.values()), 1)
        self.assertAlmostEqual(sum(observed.values()), 1)
        self.assertEqual(theory[7], 6 / 36)
        self.assertTrue(all(abs(observed[x] - theory[x]) < 0.01 for x in range(2, 13)))


if __name__ == '__main__':
    unittest.main()
