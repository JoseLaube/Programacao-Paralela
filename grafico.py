"""Benchmark de speedup do Mandelbrot com pthreads.

Compile antes com `make mandelbrot` e execute com `python3 grafico.py`.
"""

import argparse

import benchmark

# Configuração do Mandelbrot
MAX_ROW = 2300
MAX_COLUMN = 790
MAX_N = 4800

# Configuração do benchmark
MIN_THREADS = 1
MAX_THREADS = 24
REPETITIONS = 10

EXECUTABLE = "./mandelbrot"
CSV_FILE = "resultados_mandelbrot.csv"
PLOT_FILE = "grafico_aceleracao.png"


def run(num_threads):
    return benchmark.run_once(
        EXECUTABLE,
        [MAX_ROW, MAX_COLUMN, MAX_N, num_threads],
    )


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--no-show",
        action="store_true",
        help="salva o gráfico sem abrir a janela do matplotlib",
    )
    args = parser.parse_args()

    thread_counts = list(range(MIN_THREADS, MAX_THREADS + 1))

    print(f"Matriz: {MAX_ROW} x {MAX_COLUMN}")
    print(f"Máximo de iterações: {MAX_N}")
    print(f"Threads: {MIN_THREADS} até {MAX_THREADS}")
    print(f"Repetições por número de threads: {REPETITIONS}")

    results = benchmark.sweep(
        "BENCHMARK MANDELBROT - PTHREADS",
        thread_counts,
        REPETITIONS,
        run,
    )

    # O speedup usa a execução com 1 thread como referência.
    benchmark.add_speedup(results, results[MIN_THREADS]["average"])

    benchmark.print_table("Pthreads", results)
    benchmark.save_csv(CSV_FILE, results)

    speedups = [results[t]["speedup"] for t in thread_counts]

    benchmark.plot_speedup(
        {"Pthreads": (thread_counts, speedups)},
        thread_counts,
        "Speedup do Mandelbrot com Pthreads",
        PLOT_FILE,
        show=not args.no_show,
    )


if __name__ == "__main__":
    main()
