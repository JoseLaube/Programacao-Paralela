Trabalho Mandelbrot - José e Andre Fidelis

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

