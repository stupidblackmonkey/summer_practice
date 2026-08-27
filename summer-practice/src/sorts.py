import sys

# Увеличиваем лимит рекурсии для Quick Sort на больших/отсортированных массивах
sys.setrecursionlimit(2000000)


# O(n^2) 
def bubble_sort(arr: list[int]) -> list[int]:
    a = arr.copy()
    n = len(a)
    for i in range(n):
        swapped = False
        for j in range(0, n - i - 1):
            if a[j] > a[j + 1]:
                a[j], a[j + 1] = a[j + 1], a[j]
                swapped = True
        if not swapped:
            break
    return a


def selection_sort(arr: list[int]) -> list[int]:
    a = arr.copy()
    n = len(a)
    for i in range(n):
        min_idx = i
        for j in range(i + 1, n):
            if a[j] < a[min_idx]:
                min_idx = j
        a[i], a[min_idx] = a[min_idx], a[i]
    return a


def insertion_sort(arr: list[int]) -> list[int]:
    a = arr.copy()
    for i in range(1, len(a)):
        key = a[i]
        j = i - 1
        while j >= 0 and a[j] > key:
            a[j + 1] = a[j]
            j -= 1
        a[j + 1] = key
    return a


#O(n log n)
def merge_sort(arr: list[int]) -> list[int]:
    if len(arr) <= 1:
        return arr

    mid = len(arr) // 2
    left = merge_sort(arr[:mid])
    right = merge_sort(arr[mid:])

    result = []
    i = j = 0
    while i < len(left) and j < len(right):
        if left[i] <= right[j]:
            result.append(left[i])
            i += 1
        else:
            result.append(right[j])
            j += 1
    result.extend(left[i:])
    result.extend(right[j:])
    return result


def quick_sort(arr: list[int]) -> list[int]:
    if len(arr) <= 1:
        return arr
    pivot = arr[len(arr) // 2]
    left = [x for x in arr if x < pivot]
    middle = [x for x in arr if x == pivot]
    right = [x for x in arr if x > pivot]
    return quick_sort(left) + middle + quick_sort(right)


def heap_sort(arr: list[int]) -> list[int]:
    a = arr.copy()
    n = len(a)

    def heapify(length: int, i: int):
        largest = i
        left = 2 * i + 1
        right = 2 * i + 2

        if left < length and a[left] > a[largest]:
            largest = left
        if right < length and a[right] > a[largest]:
            largest = right
        if largest != i:
            a[i], a[largest] = a[largest], a[i]
            heapify(length, largest)

    for i in range(n // 2 - 1, -1, -1):
        heapify(n, i)
    for i in range(n - 1, 0, -1):
        a[i], a[0] = a[0], a[i]
        heapify(i, 0)
    return a


# O(n)
def counting_sort(arr: list[int]) -> list[int]:
    if not arr:
        return []
    min_val, max_val = min(arr), max(arr)
    count = [0] * (max_val - min_val + 1)
    for num in arr:
        count[num - min_val] += 1
    result = []
    for num_offset, c in enumerate(count):
        result.extend([num_offset + min_val] * c)
    return result


def radix_sort(arr: list[int]) -> list[int]:
    if not arr:
        return []
    shift = min(arr)
    working_arr = [x - shift for x in arr] if shift < 0 else arr.copy()

    max_val = max(working_arr)
    exp = 1
    while max_val // exp > 0:
        buckets = [[] for _ in range(10)]
        for num in working_arr:
            buckets[(num // exp) % 10].append(num)
        working_arr = [num for b in buckets for num in b]
        exp *= 10

    return [x + shift for x in working_arr] if shift < 0 else working_arr


def bucket_sort(arr: list[int]) -> list[int]:
    if not arr:
        return []
    min_val, max_val = min(arr), max(arr)
    if min_val == max_val:
        return arr.copy()

    bucket_count = max(1, len(arr) // 10)
    buckets = [[] for _ in range(bucket_count)]
    range_val = (max_val - min_val) + 1

    for num in arr:
        idx = int((num - min_val) / range_val * bucket_count)
        buckets[idx].append(num)

    result = []
    for bucket in buckets:
        result.extend(insertion_sort(bucket))
    return result


# Встроенная сортировка 
def builtin_sort(arr: list[int]) -> list[int]:
    return sorted(arr)