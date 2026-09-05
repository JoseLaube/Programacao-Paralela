Trabalho Mandelbrot - José e Andre Fidelis

##Mandelbrot Pthreads
A execução do código deve ser feita da seguinte maneira:

Compilar o mandelbrot.cpp com o seguinte comando:

g++ -O2 -pthread mandelbrot.cpp -o mandelbrot

depois rodar o script python:

python3 grafico.py

Depois esperar para executar;

A configurações do tamanho da quantidade de linhas, colunas e o máximo de iterações que pode ficar o while, estão dentro do script python

O script vai fazer 10 execuções para cada número de threads, indo de 1 até 240, totalizando 240 execuções;

A configuração da máquina que foi utilizada é um intel i7-13620H (mais informações em CPU.png e CPU2.png)
A máquina também possuí 16Gb de ram;

por fim os resultados estão apresentados no grafico_aceleracao.png, por curiosidade também tem o tempo que a 10 primeira execuções levaram e o que as 10 últimas levaram (1_thread.pgn, 24_threads.pgn).

##Mandelbrot OpenMP

Compilar o mandelbrotOmp.cpp com o seguinte comando

g++ -02 -fopenmp mandelbrotOmp.cpp -o saida

depois rodar o script python (grafico_omp.py)

python3 grafico_omp.py

(esse script além executar o código usando o as configurações do open mp com static, 1 e 120, dynamic 1 e 120 e guided, mas também vai pegar a execução do mandelbrot.cpp (resultados_mandelbrot.csv) para juntar nos gráficos)

Por fim vai ter um gráfico comparando 6 execuções e o ideal.
