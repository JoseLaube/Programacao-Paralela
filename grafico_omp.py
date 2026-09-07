"""Benchmark de speedup do Mandelbrot com OpenMP, comparado com pthreads.

Roda as cinco políticas de escalonamento pedidas, carrega o resultado já
medido com pthreads (resultados_mandelbrot.csv) e coloca tudo em um gráfico.

Compile antes com `make saida` e execute com `python3 grafico_omp.py`.
"""

import argparse
import os

import benchmark

# Configuração do Mandelbrot
MAX_ROW = 2300
MAX_COLUMN = 790
MAX_N = 4800

# Configuração do benchmark
MIN_THREADS = 1
MAX_THREADS = 16
REPETITIONS = 10

# Chunk size solicitado pelo professor
CHUNK = 120

EXECUTABLE = "./saida"
PTHREADS_CSV = "resultados_mandelbrot.csv"
PLOT_FILE = "speedup_mandelbrot_comparacao.png"

SCHEDULES = [
    ("OpenMP static,1", "static,1"),
    (f"OpenMP static,{CHUNK}", f"static,{CHUNK}"),
    ("OpenMP dynamic,1", "dynamic,1"),
    (f"OpenMP dynamic,{CHUNK}", f"dynamic,{CHUNK}"),
    ("OpenMP guided", "guided"),
]


def run(num_threads, schedule):
    """Executa o binário OpenMP com o escalonamento e o nº de threads dados."""
    env = os.environ.copy()
    env["OMP_NUM_THREADS"] = str(num_threads)
    env["OMP_SCHEDULE"] = schedule

    return benchmark.run_once(
        EXECUTABLE,
        [MAX_ROW, MAX_COLUMN, MAX_N],
        env=env,
    )


def measure_reference():
    """Tempo de referência: static,1 com 1 thread.

    As cinco configurações usam a MESMA referência, senão as curvas não
    poderiam ser comparadas entre si.
    """
    print("Referência do speedup: OpenMP static,1 com 1 thread.")
    print()

    times = []

    for repetition in range(1, REPETITIONS + 1):
        elapsed = run(1, "static,1")
        times.append(elapsed)
        print(f"Referência {repetition:2d}/{REPETITIONS} | Tempo: {elapsed:.4f} s")

    reference = sum(times) / len(times)

    print()
    print(f"Tempo de referência: {reference:.4f} s")

    return reference


def csv_name(label):
    return "resultados_" + label.replace(" ", "_").replace(",", "_") + ".csv"


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--no-show",
        action="store_true",
        help="salva o gráfico sem abrir a janela do matplotlib",
    )
    args = parser.parse_args()

    thread_counts = list(range(MIN_THREADS, MAX_THREADS + 1))

    print("=" * 70)
    print("BENCHMARK MANDELBROT - OPENMP")
    print("=" * 70)
    print(f"Matriz: {MAX_ROW} x {MAX_COLUMN}")
    print(f"Máximo de iterações: {MAX_N}")
    print(f"Threads: {MIN_THREADS} até {MAX_THREADS}")
    print(f"Repetições por cenário: {REPETITIONS}")
    print(f"Chunk: {CHUNK}")
    print()

    reference_time = measure_reference()

    all_results = {}

    for label, schedule in SCHEDULES:
        results = benchmark.sweep(
            f"CONFIGURAÇÃO: {label} (schedule={schedule})",
            thread_counts,
            REPETITIONS,
            lambda num_threads, schedule=schedule: run(num_threads, schedule),
        )

        benchmark.add_speedup(results, reference_time)
        benchmark.print_table(label, results)
        benchmark.save_csv(csv_name(label), results)

        all_results[label] = results

    # Curvas do gráfico: pthreads (já medido) + as cinco do OpenMP.
    series = {}

    pthreads_threads, pthreads_speedups = benchmark.load_csv_speedups(
        PTHREADS_CSV,
        thread_counts,
    )
    series["Pthreads"] = (pthreads_threads, pthreads_speedups)

    print()
    print(f"Pthreads: {len(pthreads_threads)} pontos carregados de {PTHREADS_CSV}")

    for label, results in all_results.items():
        speedups = [results[t]["speedup"] for t in thread_counts]
        series[label] = (thread_counts, speedups)

    benchmark.plot_speedup(
        series,
        thread_counts,
        "Speedup do Mandelbrot - Pthreads vs OpenMP",
        PLOT_FILE,
        show=not args.no_show,
    )


if __name__ == "__main__":
    main()
