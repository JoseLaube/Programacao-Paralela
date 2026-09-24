#include <complex>
#include <iostream>
#include <mpi.h>
#include <string.h>

using namespace std;

int main(int argc, char **argv){
    MPI_Init(&argc, &argv);
    int rank, size;
	MPI_Comm_rank(MPI_COMM_WORLD, &rank);
	MPI_Comm_size(MPI_COMM_WORLD, &size);

    int max_row, max_column, max_n;
    int vet_inf[3];
    if(rank == 0){
        cin >> vet_inf[0];
        cin >> vet_inf[1];
        cin >> vet_inf[2];
    }
    MPI_Bcast(vet_inf, 3, MPI_INT, 0, MPI_COMM_WORLD);

    max_row = vet_inf[0];
    max_column = vet_inf[1];
    max_n = vet_inf[2];

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
            complex<float> z (0, 0);
			int n = 0;
			while(abs(z) < 2.0f && ++n < max_n)
				z = pow(z, 2) + complex<float>(
					(float)c * 2.0f / max_column - 1.5f,
					(float)r_global * 2.0f / max_row - 1.0f
				);
			local_mat[r * max_column + c] = (n == max_n ? '#' : '.');
		}
	}
    //Gather
    MPI_Gather(local_mat, tamanho_bloco, MPI_CHAR, mat_completa, tamanho_bloco, MPI_CHAR, 0, MPI_COMM_WORLD);

    if(rank == 0){
        for(int r = 0; r < max_row; ++r){
            for(int c = 0; c < max_column; ++c)
                std::cout << mat_completa[r * max_column + c];
            cout << '\n';
        }	
        free(mat_completa);
    }
    free(local_mat);
    MPI_Finalize();
}


