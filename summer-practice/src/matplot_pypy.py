import csv
import os
import matplotlib.pyplot as plt

os.makedirs("img", exist_ok=True)

with open("benchmark_results.csv", "r", encoding="utf-8") as f:
    data = list(csv.DictReader(f))

data_types = ["Random", "Sorted", "Reversed", "Almost Sorted"]
algos = [
    "Bubble",
    "Selection",
    "Insertion",
    "Merge",
    "Quick",
    "Heap",
    "Counting",
    "Radix",
    "Bucket",
    "Built-in",
]

for d_type in data_types:
    plt.figure(figsize=(9, 5))
    for algo in algos:
        subset = [
            r
            for r in data
            if r.get("Interpreter") == "PyPy"
            and r.get("Data_Type") == d_type
            and r.get("Algorithm") == algo
            and r.get("Time_ms") not in ("N/A", None)
        ]
        if subset:
            x = [int(r["Size"]) for r in subset]
            y = [float(r["Time_ms"]) for r in subset]
            plt.plot(x, y, marker="o", label=algo)

    plt.title(f"Сортировки PyPy — {d_type}")
    plt.xlabel("Размер массива N")
    plt.ylabel("Время (мс)")
    plt.xscale("log")
    plt.yscale("log")
    plt.grid(True, ls="--")
    plt.legend(bbox_to_anchor=(1.05, 1), loc="upper left")
    plt.tight_layout()

    filename = f"img/pypy_{d_type.lower().replace(' ', '_')}_time.png"
    plt.savefig(filename)
    plt.close()

print(
    "Готово! Графики для PyPy созданы в папке img/ (с префиксом pypy_*_time.png)"
)