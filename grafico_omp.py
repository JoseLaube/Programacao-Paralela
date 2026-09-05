import subprocess
import time
import csv
import os
import matplotlib.pyplot as plt


# ============================================================
# Configuração do Mandelbrot
# ============================================================

MAX_ROW = 2300
MAX_COLUMN = 790
MAX_N = 4800


# ============================================================
# Configuração do benchmark
# ============================================================

MIN_THREADS = 1
MAX_THREADS = 16
REPETITIONS = 10

# Chunk size solicitado pelo professor
N = 120


# ============================================================
# Configurações OpenMP
# ============================================================

OPENMP_CONFIGS = [
    ("OpenMP static,1", "static,1"),
    ("OpenMP static,120", "static,120"),
    ("OpenMP dynamic,1", "dynamic,1"),
    ("OpenMP dynamic,120", "dynamic,120"),
    ("OpenMP guided", "guided")
]


# ============================================================
# Executa uma vez
# ============================================================

def run_program(num_threads, schedule):
    """
    Executa o Mandelbrot uma vez utilizando OpenMP.

    num_threads:
        Número de threads utilizadas.

    schedule:
        Configuração do escalonamento OpenMP.

    Retorna:
        Tempo de execução em segundos.
    """

    input_data = (
        f"{MAX_ROW}\n"
        f"{MAX_COLUMN}\n"
        f"{MAX_N}\n"
    )

    # Copia as variáveis de ambiente atuais
    env = os.environ.copy()

    # Define as configurações do OpenMP
    env["OMP_NUM_THREADS"] = str(num_threads)
    env["OMP_SCHEDULE"] = schedule

    start = time.perf_counter()

    subprocess.run(
        ["./saida"],
        input=input_data,
        text=True,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.PIPE,
        check=True,
        env=env
    )

    end = time.perf_counter()

    return end - start


# ============================================================
# Executa o benchmark de uma configuração OpenMP
# ============================================================

def benchmark_config(name, schedule):

    results = {}

    total_runs = (
        (MAX_THREADS - MIN_THREADS + 1)
        * REPETITIONS
    )

    current_run = 0

    print("\n")
    print("=" * 70)
    print(f"CONFIGURAÇÃO: {name}")
    print("=" * 70)
    print(f"Schedule: {schedule}")
    print(f"Total de execuções: {total_runs}")
    print()

    for num_threads in range(
        MIN_THREADS,
        MAX_THREADS + 1
    ):

        times = []

        print(
            f"===== {num_threads} thread(s) ====="
        )

        for repetition in range(
            1,
            REPETITIONS + 1
        ):

            current_run += 1

            elapsed = run_program(
                num_threads,
                schedule
            )

            times.append(elapsed)

            print(
                f"Execução {repetition:2d}/{REPETITIONS} "
                f"| Tempo: {elapsed:.4f} s "
                f"| Progresso: "
                f"{current_run}/{total_runs}"
            )

        # Calcula a média das 10 execuções
        average = sum(times) / len(times)

        results[num_threads] = {
            "times": times,
            "average": average
        }

        print(
            f"Média: {average:.4f} s"
        )
        print()

    return results


# ============================================================
# Calcula o speedup
# ============================================================

def calculate_speedup(results, reference_time):

    for num_threads in results:

        average = results[num_threads]["average"]

        results[num_threads]["speedup"] = (
            reference_time / average
        )


# ============================================================
# Salva resultados em CSV
# ============================================================

def save_csv(filename, results):

    with open(
        filename,
        "w",
        newline=""
    ) as file:

        writer = csv.writer(file)

        writer.writerow([
            "threads",
            "tempo_medio",
            "speedup"
        ])

        for num_threads in sorted(results):

            writer.writerow([
                num_threads,
                results[num_threads]["average"],
                results[num_threads]["speedup"]
            ])


# ============================================================
# Lê resultados antigos do Pthreads
# ============================================================

def load_pthreads():

    threads = []
    speedups = []

    with open(
        "resultados_mandelbrot.csv",
        "r"
    ) as file:

        reader = csv.DictReader(file)

        for row in reader:

            num_threads = int(
                row["threads"]
            )

            # Usar somente 1 até 16 threads
            if MIN_THREADS <= num_threads <= MAX_THREADS:

                threads.append(num_threads)

                speedups.append(
                    float(row["speedup"])
                )

    return threads, speedups


# ============================================================
# Mostra resultados
# ============================================================

def print_results(name, results):

    print("\n")
    print("=" * 70)
    print(f"RESULTADOS: {name}")
    print("=" * 70)

    print(
        f"{'Threads':>8}"
        f"{'Média (s)':>15}"
        f"{'Speedup':>15}"
    )

    print("-" * 40)

    for num_threads in sorted(results):

        average = results[num_threads]["average"]
        speedup = results[num_threads]["speedup"]

        print(
            f"{num_threads:>8}"
            f"{average:>15.4f}"
            f"{speedup:>15.4f}"
        )


# ============================================================
# Função principal
# ============================================================

def main():

    # ========================================================
    # Referência para o speedup
    # ========================================================
    #
    # Primeiro executamos static,1 com 1 thread.
    #
    # Essa execução será usada como referência comum
    # para calcular o speedup das cinco configurações.
    #
    # Isso permite comparar as curvas entre si.
    # ========================================================

    print("=" * 70)
    print("BENCHMARK MANDELBROT - OPENMP")
    print("=" * 70)
    print()
    print(
        "CPU: 10 núcleos físicos / 16 threads"
    )
    print(
        f"Matriz: {MAX_ROW} x {MAX_COLUMN}"
    )
    print(
        f"Máximo de iterações: {MAX_N}"
    )
    print(
        f"Repetições por cenário: {REPETITIONS}"
    )
    print(
        f"Threads: {MIN_THREADS} até {MAX_THREADS}"
    )
    print(
        f"Chunk N: {N}"
    )
    print()

    print(
        "A referência do speedup será obtida "
        "com OpenMP static,1 usando 1 thread."
    )
    print()

    reference_times = []

    for repetition in range(
        1,
        REPETITIONS + 1
    ):

        elapsed = run_program(
            1,
            "static,1"
        )

        reference_times.append(elapsed)

        print(
            f"Referência {repetition:2d}/{REPETITIONS}"
            f" | Tempo: {elapsed:.4f} s"
        )

    reference_time = (
        sum(reference_times)
        / len(reference_times)
    )

    print()
    print(
        f"Tempo de referência: "
        f"{reference_time:.4f} s"
    )
    print()

    # ========================================================
    # Executar os 5 cenários OpenMP
    # ========================================================

    all_results = {}

    for name, schedule in OPENMP_CONFIGS:

        # Evita executar novamente a referência
        # static,1 com 1 thread.
        #
        # Porém, para manter 10 execuções para cada
        # configuração/thread, benchmark_config ainda
        # executará normalmente essa configuração.

        results = benchmark_config(
            name,
            schedule
        )

        # Speedup utilizando a MESMA referência
        calculate_speedup(
            results,
            reference_time
        )

        all_results[name] = results

        # Salvar CSV individual
        filename = (
            name
            .replace(" ", "_")
            .replace(",", "_")
        )

        save_csv(
            f"resultados_{filename}.csv",
            results
        )

        print_results(
            name,
            results
        )

    # ========================================================
    # Carregar Pthreads
    # ========================================================

    print("\n")
    print("=" * 70)
    print("CARREGANDO RESULTADOS PTHREADS")
    print("=" * 70)

    pthreads_threads, pthreads_speedup = (
        load_pthreads()
    )

    print(
        f"Pthreads: {len(pthreads_threads)} "
        f"pontos carregados (1-16 threads)"
    )

    # ========================================================
    # Gráfico
    # ========================================================

    threads = list(
        range(
            MIN_THREADS,
            MAX_THREADS + 1
        )
    )

    plt.figure(
        figsize=(12, 7)
    )

    # --------------------------------------------------------
    # Speedup ideal
    # --------------------------------------------------------

    plt.plot(
        threads,
        threads,
        linestyle="--",
        label="Ideal"
    )

    # --------------------------------------------------------
    # Pthreads
    # --------------------------------------------------------

    plt.plot(
        pthreads_threads,
        pthreads_speedup,
        marker="o",
        label="Pthreads"
    )

    # --------------------------------------------------------
    # OpenMP
    # --------------------------------------------------------

    for name, results in all_results.items():

        speedups = [
            results[t]["speedup"]
            for t in threads
        ]

        plt.plot(
            threads,
            speedups,
            marker="o",
            label=name
        )

    # --------------------------------------------------------
    # Configurações do gráfico
    # --------------------------------------------------------

    plt.xlabel(
        "Número de Threads"
    )

    plt.ylabel(
        "Speedup"
    )

    plt.title(
        "Speedup do Mandelbrot - Pthreads vs OpenMP\n"
        "CPU: 10 núcleos físicos / 16 threads"
    )

    plt.xticks(
        threads
    )

    plt.grid(
        True
    )

    plt.legend()

    plt.tight_layout()

    plt.savefig(
        "speedup_mandelbrot_comparacao.png",
        dpi=300
    )

    plt.show()


# ============================================================
# Execução
# ============================================================

if __name__ == "__main__":
    main()