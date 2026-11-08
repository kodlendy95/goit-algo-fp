"""Завдання 1: однозв'язний список, реверс, сортування вставками та злиття."""
from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable, Optional


@dataclass
class Node:
    value: int
    next: Optional[Node] = None


class LinkedList:
    def __init__(self, values: Iterable[int] = ()) -> None:
        self.head: Optional[Node] = None
        self.tail: Optional[Node] = None
        for value in values:
            self.append(value)

    def append(self, value: int) -> None:
        node = Node(value)
        if self.head is None:
            self.head = self.tail = node
        else:
            assert self.tail is not None
            self.tail.next = node
            self.tail = node

    def to_list(self) -> list[int]:
        result = []
        current = self.head
        while current is not None:
            result.append(current.value)
            current = current.next
        return result

    def reverse(self) -> None:
        """O(n) за часом, O(1) за пам'яттю; змінює саме посилання вузлів."""
        previous: Optional[Node] = None
        current = self.head
        self.tail = current
        while current is not None:
            next_node = current.next
            current.next = previous
            previous = current
            current = next_node
        self.head = previous

    def insertion_sort(self) -> None:
        """Сортування вставками, змінює зв'язки, а не значення вузлів: O(n²)."""
        sorted_head: Optional[Node] = None
        current = self.head
        while current is not None:
            next_node = current.next
            if sorted_head is None or current.value < sorted_head.value:
                current.next = sorted_head
                sorted_head = current
            else:
                scan = sorted_head
                while scan.next is not None and scan.next.value <= current.value:
                    scan = scan.next
                current.next = scan.next
                scan.next = current
            current = next_node

        self.head = sorted_head
        self.tail = sorted_head
        while self.tail is not None and self.tail.next is not None:
            self.tail = self.tail.next


def merge_sorted_lists(first: LinkedList, second: LinkedList) -> LinkedList:
    """O(n + m). Вхідні списки зберігаються без змін; кожен має бути відсортований."""
    merged = LinkedList()
    left, right = first.head, second.head
    while left is not None and right is not None:
        if left.value <= right.value:
            merged.append(left.value)
            left = left.next
        else:
            merged.append(right.value)
            right = right.next
    while left is not None:
        merged.append(left.value)
        left = left.next
    while right is not None:
        merged.append(right.value)
        right = right.next
    return merged


def main() -> None:
    numbers = LinkedList([4, 2, 7, 1, 5, 3])
    print('Початковий список:', numbers.to_list())
    numbers.reverse()
    print('Після реверсування:', numbers.to_list())
    numbers.insertion_sort()
    print('Після сортування:', numbers.to_list())

    other = LinkedList([0, 2, 6, 8])
    combined = merge_sorted_lists(numbers, other)
    print('Другий відсортований:', other.to_list())
    print('Результат об’єднання:', combined.to_list())


if __name__ == '__main__':
    main()
