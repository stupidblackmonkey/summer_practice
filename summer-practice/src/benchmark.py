import csv
import os
import random
import sys
import time

import sorts

# Проверяем, в каком движке запущен скрипт
IS_PYPY = "__pypy__" in sys.builtin_module_names
ENGINE = "PyPy" if IS_PYPY else "CPython"

# tracemalloc используем только в CPython
if not IS_PYPY:
    import tracemalloc
    import matplotlib.pyplot as plt

SIZES = [10, 500, 1000, 50000, 1000000]
DATA_TYPES = ["Random", "Sorted", "Reversed", "Almost Sorted"]
O_N2_LIMIT = 1000

ALGORITHMS = {
    "Bubble": sorts.bubble_sort,
    "Selection": sorts.selection_sort,
    "Insertion": sorts.insertion_sort,
    "Merge": sorts.merge_sort,
    "Quick": sorts.quick_sort,
    "Heap": sorts.heap_sort,
    "Counting": sorts.counting_sort,
    "Radix": sorts.radix_sort,
    "Bucket": sorts.bucket_sort,
    "Built-in": sorts.builtin_sort,
}


def generate_data(size, data_type):
    if data_type == "Random":
        return [random.randint(0, size * 2) for _ in range(size)]
    elif data_type == "Sorted":
        return list(range(size))
    elif data_type == "Reversed":
        return list(range(size, 0, -1))
    elif data_type == "Almost Sorted":
        arr = list(range(size))
        for _ in range(max(1, int(size * 0.05))):
            i, j = random.randint(0, size - 1), random.randint(0, size - 1)
            arr[i], arr[j] = arr[j], arr[i]
        return arr


def run():
    print(f"=== Запуск замеров для: {ENGINE} ===")
    results = []

    for d_type in DATA_TYPES:
        for size in SIZES:
            data = generate_data(size, d_type)
            for name, func in ALGORITHMS.items():
                if (
                    name in ["Bubble", "Selection", "Insertion"]
                    and size > O_N2_LIMIT
                ):
                    results.append(
                        {
                            "OS": "Win",
                            "Interpreter": ENGINE,
                            "Data_Type": d_type,
                            "Algorithm": name,
                            "Size": size,
                            "Time_ms": "N/A",
                            "Memory_KB": "N/A",
                        }
                    )
                    continue

                if not IS_PYPY:
                    tracemalloc.start()

                t0 = time.perf_counter()
                _ = func(data)
                t1 = time.perf_counter()

                mem_kb = "N/A"
                if not IS_PYPY:
                    _, peak = tracemalloc.get_traced_memory()
                    tracemalloc.stop()
                    mem_kb = round(peak / 1024, 3)

                results.append(
                    {
                        "OS": "Win",
                        "Interpreter": ENGINE,
                        "Data_Type": d_type,
                        "Algorithm": name,
                        "Size": size,
                        "Time_ms": round((t1 - t0) * 1000, 3),
                        "Memory_KB": mem_kb,
                    }
                )

    # Запись в общий CSV-файл
    csv_file = "benchmark_results.csv"
    file_exists = os.path.isfile(csv_file)
    with open(csv_file, "a", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=results[0].keys())
        if not file_exists:
            writer.writeheader()
        writer.writerows(results)

    # Генерация графиков (только при запуске обычного Python)
    if not IS_PYPY:
        os.makedirs("img", exist_ok=True)
        for d_type in DATA_TYPES:
            plt.figure(figsize=(9, 5))
            for algo in ALGORITHMS.keys():
                subset = [
                    r
                    for r in results
                    if r["Data_Type"] == d_type
                    and r["Algorithm"] == algo
                    and r["Time_ms"] != "N/A"
                ]
                if subset:
                    plt.plot(
                        [r["Size"] for r in subset],
                        [r["Time_ms"] for r in subset],
                        marker="o",
                        label=algo,
                    )
            plt.title(f"Сортировки — {d_type}")
            plt.xlabel("Размер массива N")
            plt.ylabel("Время (мс)")
            plt.xscale("log")
            plt.yscale("log")
            plt.grid(True, ls="--")
            plt.legend(bbox_to_anchor=(1.05, 1), loc="upper left")
            plt.tight_layout()
            plt.savefig(f"img/{d_type.lower().replace(' ', '_')}_time.png")
            plt.close()

    print(f"Готово для {ENGINE}!")


if __name__ == "__main__":
    run()