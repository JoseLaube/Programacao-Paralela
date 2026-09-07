# Compilação do trabalho de Mandelbrot.
#
#   make          compila as duas versões
#   make mandelbrot   apenas a versão com pthreads
#   make saida        apenas a versão com OpenMP
#   make clean        remove os binários

CXX      ?= g++
CXXFLAGS ?= -O2 -Wall -Wextra
OMPFLAGS ?= -fopenmp

all: mandelbrot saida

mandelbrot: mandelbrot.cpp mandelbrot.hpp
	$(CXX) $(CXXFLAGS) -pthread mandelbrot.cpp -o mandelbrot

saida: mandelbrotOmp.cpp mandelbrot.hpp
	$(CXX) $(CXXFLAGS) $(OMPFLAGS) mandelbrotOmp.cpp -o saida

clean:
	rm -f mandelbrot saida

.PHONY: all clean
