"""Rotinas comuns aos benchmarks do Mandelbrot (pthreads e OpenMP).

Concentra aqui tudo o que grafico.py e grafico_omp.py fariam duas vezes:
executar o binário, varrer números de threads, calcular speedup, salvar CSV,
imprimir tabela e desenhar o gráfico.
"""

import csv
import re
import subprocess
import time

import matplotlib.pyplot as plt

# Linha que os binários escrevem em stderr, ex.: "tempo_calculo: 12.345678"
TIME_PATTERN = re.compile(r"tempo_calculo:\s*([0-9.eE+-]+)")


def run_once(executable, stdin_values, env=None):
    """Executa o binário uma vez e devolve o tempo do cálculo em segundos.

    Prefere o tempo medido dentro do programa, que exclui o custo de subir o
    processo e de alocar a matriz. Se o binário não reportar nada, cai para o
    relógio externo.
    """
    payload = "".join(f"{value}\n" for value in stdin_values)

    start = time.perf_counter()

    completed = subprocess.run(
        [executable],
        input=payload,
        text=True,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.PIPE,
        check=True,
        env=env,
    )

    wall_clock = time.perf_counter() - start

    match = TIME_PATTERN.search(completed.stderr or "")

    return float(match.group(1)) if match else wall_clock


def sweep(label, thread_counts, repetitions, run):
    """Mede `repetitions` execuções para cada número de threads.

    run: função que recebe o número de threads e devolve o tempo em segundos.
    Devolve {num_threads: {"times": [...], "average": float}}.
    """
    results = {}
    total = len(thread_counts) * repetitions
    done = 0

    print()
    print("=" * 70)
    print(label)
    print("=" * 70)
    print(f"Total de execuções: {total}")
    print()

    for num_threads in thread_counts:
        times = []

        print(f"===== {num_threads} thread(s) =====")

        for repetition in range(1, repetitions + 1):
            elapsed = run(num_threads)
            times.append(elapsed)
            done += 1

            print(
                f"Execução {repetition:2d}/{repetitions} "
                f"| Tempo: {elapsed:.4f} s "
                f"| Progresso: {done}/{total}"
            )

        average = sum(times) / len(times)
        results[num_threads] = {"times": times, "average": average}

        print(f"Média: {average:.4f} s")
        print()

    return results


def add_speedup(results, reference_time):
    """Acrescenta a chave "speedup" a cada entrada, relativa a reference_time."""
    for entry in results.values():
        entry["speedup"] = reference_time / entry["average"]


def print_table(label, results):
    print()
    print("=" * 70)
    print(f"RESULTADOS: {label}")
    print("=" * 70)
    print(f"{'Threads':>8}{'Média (s)':>15}{'Speedup':>15}")
    print("-" * 38)

    for num_threads in sorted(results):
        entry = results[num_threads]
        print(
            f"{num_threads:>8}"
            f"{entry['average']:>15.4f}"
            f"{entry['speedup']:>15.4f}"
        )


def save_csv(filename, results):
    with open(filename, "w", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(["threads", "tempo_medio", "speedup"])

        for num_threads in sorted(results):
            entry = results[num_threads]
            writer.writerow([num_threads, entry["average"], entry["speedup"]])

    print(f"Resultados salvos em: {filename}")


def load_csv_speedups(filename, thread_counts):
    """Lê um CSV já gerado e devolve (threads, speedups) filtrado."""
    wanted = set(thread_counts)
    threads = []
    speedups = []

    with open(filename, newline="") as file:
        for row in csv.DictReader(file):
            num_threads = int(row["threads"])

            if num_threads in wanted:
                threads.append(num_threads)
                speedups.append(float(row["speedup"]))

    return threads, speedups


def plot_speedup(series, thread_counts, title, filename, show=True):
    """Desenha as curvas de speedup junto com a reta do speedup ideal.

    series: {rótulo: (lista_de_threads, lista_de_speedups)}
    """
    plt.figure(figsize=(12, 7))

    plt.plot(thread_counts, thread_counts, linestyle="--", label="Ideal")

    for label, (threads, speedups) in series.items():
        plt.plot(threads, speedups, marker="o", label=label)

    plt.xlabel("Número de Threads")
    plt.ylabel("Speedup")
    plt.title(title)
    plt.xticks(thread_counts)
    plt.grid(True)
    plt.legend()
    plt.tight_layout()
    plt.savefig(filename, dpi=300)

    print(f"Gráfico salvo em: {filename}")

    if show:
        plt.show()
