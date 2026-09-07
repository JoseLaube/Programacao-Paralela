// Mandelbrot paralelizado com pthreads.
//
// Cada thread recebe uma faixa contígua de linhas da matriz. Como o custo por
// linha varia bastante (linhas no centro do conjunto iteram até max_iter), a
// divisão em blocos iguais é justamente o que o benchmark quer avaliar.
//
// Entrada (stdin): linhas, colunas, max_iter, n_threads
// Saída: tempo do cálculo em stderr; a matriz em stdout apenas com --print

#include "mandelbrot.hpp"

#include <pthread.h>

#include <chrono>
#include <cstddef>
#include <iostream>
#include <string>
#include <vector>

namespace {

// Faixa de linhas [first_row, last_row) atribuída a uma thread.
struct ThreadTask {
	Params params;
	char *grid;
	int first_row;
	int last_row;
};

// Adapta render_rows à assinatura exigida por pthread_create.
void *worker(void *arg) {
	const ThreadTask *task = static_cast<const ThreadTask *>(arg);

	render_rows(task->params, task->grid, task->first_row, task->last_row);

	return nullptr;
}

// Divide as linhas em n_threads faixas de tamanho equilibrado.
std::vector<ThreadTask> split_rows(const Params &p, char *grid, int n_threads) {
	std::vector<ThreadTask> tasks((std::size_t)n_threads);

	for (int i = 0; i < n_threads; ++i) {
		tasks[i].params = p;
		tasks[i].grid = grid;
		tasks[i].first_row = (int)((long long)i * p.rows / n_threads);
		tasks[i].last_row = (int)((long long)(i + 1) * p.rows / n_threads);
	}

	return tasks;
}

// Dispara uma thread por tarefa e espera todas terminarem.
void run_parallel(std::vector<ThreadTask> &tasks) {
	std::vector<pthread_t> threads(tasks.size());

	std::size_t created = 0;
	int status = 0;

	for (; created < tasks.size(); ++created) {
		status = pthread_create(&threads[created], nullptr, worker, &tasks[created]);

		if (status != 0)
			break;
	}

	// Junta o que foi criado antes de propagar o erro: as tarefas vivem na
	// pilha de main e não podem ser destruídas com threads ainda rodando.
	for (std::size_t i = 0; i < created; ++i)
		pthread_join(threads[i], nullptr);

	if (status != 0)
		throw std::runtime_error(
			"falha ao criar thread: " + std::string(std::strerror(status))
		);
}

int read_thread_count(std::istream &in) {
	int n_threads = 0;

	if (!(in >> n_threads) || n_threads <= 0)
		throw std::runtime_error(
			"número de threads inválido: esperado um inteiro positivo"
		);

	return n_threads;
}

}  // namespace

int main(int argc, char **argv) {
	try {
		const Params params = read_params(std::cin);
		const int n_threads = read_thread_count(std::cin);

		// Um único bloco contíguo: uma linha começa onde a anterior termina,
		// o que preserva a localidade de cache entre linhas vizinhas.
		std::vector<char> grid((std::size_t)params.rows * params.cols);

		std::vector<ThreadTask> tasks = split_rows(params, grid.data(), n_threads);

		const auto start = std::chrono::steady_clock::now();
		run_parallel(tasks);
		const auto end = std::chrono::steady_clock::now();

		report_time(std::chrono::duration<double>(end - start).count());

		if (wants_grid_output(argc, argv))
			print_grid(params, grid.data(), std::cout);

		return 0;
	} catch (const std::exception &e) {
		std::cerr << "erro: " << e.what() << '\n';
		return 1;
	}
}
