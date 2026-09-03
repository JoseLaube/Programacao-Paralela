import subprocess
import time
import csv
import matplotlib.pyplot as plt

# Configuração do Mandelbrot
MAX_ROW = 2300
MAX_COLUMN = 790
MAX_N = 4800

# Configuração do benchmark
MIN_THREADS = 1
MAX_THREADS = 24
REPETITIONS = 10

# Nome do executável
EXECUTABLE = "./mandelbrot"


def run_program(num_threads):
    """
    Executa o Mandelbrot uma vez e retorna o tempo de execução em segundos.
    """

    input_data = (
        f"{MAX_ROW}\n"
        f"{MAX_COLUMN}\n"
        f"{MAX_N}\n"
        f"{num_threads}\n"
    )

    start = time.perf_counter()

    subprocess.run(
        [EXECUTABLE],
        input=input_data,
        text=True,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.PIPE,
        check=True
    )

    end = time.perf_counter()

    return end - start


def main():

    results = {}

    total_runs = (
        (MAX_THREADS - MIN_THREADS + 1)
        * REPETITIONS
    )

    current_run = 0

    print("Iniciando benchmark...")
    print(f"Total de execuções: {total_runs}")
    print()

    for num_threads in range(MIN_THREADS, MAX_THREADS + 1):

        times = []

        print(f"===== {num_threads} thread(s) =====")

        for repetition in range(1, REPETITIONS + 1):

            current_run += 1

            elapsed = run_program(num_threads)
            times.append(elapsed)

            print(
                f"Execução {repetition:2d}/{REPETITIONS} "
                f"| Tempo: {elapsed:.4f} s "
                f"| Progresso: {current_run}/{total_runs}"
            )

        average = sum(times) / len(times)

        results[num_threads] = {
            "times": times,
            "average": average
        }

        print(f"Média: {average:.4f} s")
        print()

    # Tempo da execução com 1 thread
    time_1_thread = results[1]["average"]

    # Calcular speedup
    for num_threads in results:

        average = results[num_threads]["average"]

        results[num_threads]["speedup"] = (
            time_1_thread / average
        )

    # Mostrar resultados
    print("\n================ RESULTADOS ================\n")

    print(
        f"{'Threads':>8} "
        f"{'Média (s)':>12} "
        f"{'Speedup':>12}"
    )

    print("-" * 36)

    for num_threads in results:

        average = results[num_threads]["average"]
        speedup = results[num_threads]["speedup"]

        print(
            f"{num_threads:>8} "
            f"{average:>12.4f} "
            f"{speedup:>12.4f}"
        )

    # Salvar CSV
    with open("resultados_mandelbrot.csv", "w", newline="") as file:

        writer = csv.writer(file)

        writer.writerow([
            "threads",
            "tempo_medio",
            "speedup"
        ])

        for num_threads in results:

            writer.writerow([
                num_threads,
                results[num_threads]["average"],
                results[num_threads]["speedup"]
            ])

    print("\nResultados salvos em:")
    print("resultados_mandelbrot.csv")

    # ============================
    # Gráfico
    # ============================

    threads = list(results.keys())
    speedups = [
        results[t]["speedup"]
        for t in threads
    ]

    plt.figure(figsize=(10, 6))

    plt.plot(
        threads,
        speedups,
        marker="o"
    )

    # Speedup ideal
    plt.plot(
        threads,
        threads,
        linestyle="--",
        label="Speedup ideal"
    )

    plt.xlabel("Número de Threads")
    plt.ylabel("Speedup")

    plt.title(
        "Speedup do Mandelbrot com Pthreads"
    )

    plt.xticks(threads)

    plt.grid(True)

    plt.legend()

    plt.tight_layout()

    plt.savefig(
        "speedup_mandelbrot.png",
        dpi=300
    )

    plt.show()


if __name__ == "__main__":
    main()