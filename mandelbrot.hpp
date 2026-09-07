// Núcleo compartilhado pelas duas versões do trabalho (pthreads e OpenMP).
//
// Manter o cálculo em um único lugar garante que os dois binários façam
// exatamente a mesma conta: a diferença de tempo entre eles vem apenas da
// forma de escalonar as linhas, que é o que o trabalho quer medir.

#ifndef MANDELBROT_HPP
#define MANDELBROT_HPP

#include <complex>
#include <cstddef>
#include <cstdio>
#include <cstring>
#include <istream>
#include <ostream>
#include <stdexcept>

// Parâmetros da imagem a ser gerada.
struct Params {
	int rows;      // linhas da matriz
	int cols;      // colunas da matriz
	int max_iter;  // teto de iterações por ponto
};

// Quantas iterações o ponto (row, col) suporta antes de escapar do conjunto.
// Retorna max_iter quando o ponto não escapa, ou seja, pertence ao conjunto.
inline int escape_iterations(const Params &p, int row, int col) {
	const std::complex<float> c(
		(float)col * 2 / p.cols - 1.5f,
		(float)row * 2 / p.rows - 1.0f
	);

	std::complex<float> z;
	int n = 0;

	// norm(z) < 4 equivale a abs(z) < 2, mas sem calcular a raiz quadrada.
	// z * z também substitui pow(z, 2), que promoveria a conta para double.
	while (std::norm(z) < 4.0f && ++n < p.max_iter)
		z = z * z + c;

	return n;
}

// Preenche as linhas [first_row, last_row) da matriz.
// A matriz é um bloco contíguo de rows * cols bytes.
inline void render_rows(const Params &p, char *grid, int first_row, int last_row) {
	for (int r = first_row; r < last_row; ++r) {
		char *line = grid + (std::size_t)r * p.cols;

		for (int c = 0; c < p.cols; ++c)
			line[c] = (escape_iterations(p, r, c) == p.max_iter) ? '#' : '.';
	}
}

// Lê linhas, colunas e máximo de iterações da entrada padrão.
inline Params read_params(std::istream &in) {
	Params p{};

	if (!(in >> p.rows >> p.cols >> p.max_iter))
		throw std::runtime_error(
			"entrada inválida: esperado linhas, colunas e max_iter"
		);

	if (p.rows <= 0 || p.cols <= 0 || p.max_iter <= 0)
		throw std::runtime_error(
			"linhas, colunas e max_iter devem ser positivos"
		);

	return p;
}

// Desenha a matriz em ASCII. Usado apenas com a flag --print, para conferir
// visualmente o resultado; os benchmarks rodam sem imprimir nada.
inline void print_grid(const Params &p, const char *grid, std::ostream &out) {
	for (int r = 0; r < p.rows; ++r) {
		out.write(grid + (std::size_t)r * p.cols, p.cols);
		out.put('\n');
	}
}

// Reporta o tempo do cálculo em stderr, deixando stdout livre para a matriz.
// Os scripts de benchmark leem esta linha.
inline void report_time(double seconds) {
	std::fprintf(stderr, "tempo_calculo: %.6f\n", seconds);
}

inline bool wants_grid_output(int argc, char **argv) {
	for (int i = 1; i < argc; ++i)
		if (std::strcmp(argv[i], "--print") == 0)
			return true;

	return false;
}

#endif  // MANDELBROT_HPP
