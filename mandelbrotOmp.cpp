// Mandelbrot paralelizado com OpenMP.
//
// O laço externo usa schedule(runtime), então a política de escalonamento é
// escolhida pela variável de ambiente OMP_SCHEDULE, definida por grafico_omp.py
// (static,1 / static,120 / dynamic,1 / dynamic,120 / guided).
//
// Entrada (stdin): linhas, colunas, max_iter
// Threads: variável de ambiente OMP_NUM_THREADS
// Saída: tempo do cálculo em stderr; a matriz em stdout apenas com --print

#include "mandelbrot.hpp"

#include <chrono>
#include <cstddef>
#include <iostream>
#include <vector>

int main(int argc, char **argv) {
	try {
		const Params params = read_params(std::cin);

		// Mesmo bloco contíguo da versão com pthreads. Alocar linha a linha
		// mudaria a localidade de cache e tornaria a comparação injusta.
		std::vector<char> grid((std::size_t)params.rows * params.cols);
		char *data = grid.data();

		const int rows = params.rows;

		const auto start = std::chrono::steady_clock::now();

#pragma omp parallel for schedule(runtime)
		for (int r = 0; r < rows; ++r)
			render_rows(params, data, r, r + 1);

		const auto end = std::chrono::steady_clock::now();

		report_time(std::chrono::duration<double>(end - start).count());

		if (wants_grid_output(argc, argv))
			print_grid(params, data, std::cout);

		return 0;
	} catch (const std::exception &e) {
		std::cerr << "erro: " << e.what() << '\n';
		return 1;
	}
}
