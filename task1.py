# Реалізуйте функцію, яка знаходить максимальний та мінімальний елементи в масиві, використовуючи метод «розділяй і володарюй».
# Функція приймає масив чисел довільної довжини (10 б).
# Використано рекурсивний підхід (10 б).
# Повертається кортеж значень (мінімум, максимум) (10 б).
# Складність алгоритму — O(n) (10 б).

import math


def min_max_values(arr):
    if len(arr) < 2:
        return "Array must contain at least two elements"

    if len(arr) == 2:
        return (min(arr[0], arr[1]), max(arr[0], arr[1]))

    mid = len(arr) // 2

    left = arr[:mid]
    right = arr[mid:]

    left_min, left_max = min_max_values(left)
    right_min, right_max = min_max_values(right)
    min_digit, max_digit = (min(left_min, right_min), max(left_max, right_max))
    return (min_digit, max_digit)


array = [3, 5, 1, 8, 2, 7, 4, 6]
print(f"Min: {min_max_values(array)[0]}, Max: {min_max_values(array)[1]}")
