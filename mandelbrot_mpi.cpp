#include <complex>
#include <iostream>
#include <mpi.h>
#include <string.h>

using namespace std;

int main(){
    MPI_Init(&argc, &argv);
    int rank, size;
	MPI_Comm_rank(MPI_COMM_WORLD, &rank);
	MPI_Comm_size(MPI_COMM_WORLD, &size);

    int max_row, max_column, max_n;
    if(rank == 0){
        cin >> max_row;
        cin >> max_column;
        cin >> max_n;
    }

    vet_inf[3] = [max_row, max_column, max_n];

    int MPI_Bcast(vet_inf, 3, MPI_INT, 0, MPI_COMM_WORLD);

    int linhas = max_row/size;
    int tamanho_bloco = linhas * max_column; 

    char *local_mat = (char*) malloc(sizeof(char) * tamanho_bloco);

    char *mat_completa = NULL;
    if (rank == 0) {
        mat_completa = (char*) malloc(sizeof(char) * (max_row * max_column));
    }


    for(int r = 0; r < linhas; ++r){
        int r_global = (rank * linhas) + r;
        
        for(int c = 0; c < max_column; ++c){
            //para cada celula da matriz
            complex<float> z;
			int n = 0;
			while(abs(z) < 2 && ++n < max_n)
				z = pow(z, 2) + decltype(z)(
					(float)c * 2 / max_column - 1.5,
					(float)r_global * 2 / max_row - 1
				);
			local_mat[r * max_column + c] = (n == max_n ? '#' : '.');
		}
	}
    //Getter


    //Só o 0 imprime
	for(int r = 0; r < max_row; ++r){
		for(int c = 0; c < max_column; ++c)
			std::cout << mat[r][c];
		cout << '\n';
	}	
}


