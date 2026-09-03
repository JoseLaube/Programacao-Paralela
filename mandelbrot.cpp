#include <complex>
#include <iostream>

using namespace std;

struct thread_data {
	int max_row;
	int max_column;
	int max_n;
	int n_threads;
	char **mat;
	int ini_row;
	int fin_row;
	int t_id;
};

void *mandel_thread(void *a){
	struct thread_data *data = (struct thread_data *)a;
	//abre os dados 
	int max_row = data->max_row;
	int max_column = data->max_column;
	int max_n = data->max_n;
	int n = data->max_n;

	//for(int r = 0; r < max_row; ++r){ //escalonemento
	for(int r = data->ini_row; r < data->fin_row; ++r){
		for(int c = 0; c < max_column; ++c){
			//para cada celula da matriz
			complex<float> z;
			int n = 0;
			while(abs(z) < 2 && ++n < max_n)
				z = pow(z, 2) + decltype(z)(
					(float)c * 2 / max_column - 1.5,
					(float)r * 2 / max_row - 1
				);
			data->mat[r][c]=(n == max_n ? '#' : '.');
		}
	}
	pthread_exit(NULL);
}

int main(){
	int max_row, max_column, max_n, n_threads;
	cin >> max_row;
	cin >> max_column;
	cin >> max_n;
	cin >> n_threads;

	char **mat = (char**)malloc(sizeof(char*)*max_row);
	char *block = (char *)malloc(sizeof(char)*max_row*max_column);

	for (int i=0; i<max_row;i++) {
		mat[i]=&block[i * max_column];
//		mat[i]=(char*)malloc(sizeof(char)*max_column);
	}
	// alimentar a memoria
	// criar as threads

	pthread_t threads[n_threads];

	struct thread_data data[n_threads];

	for (int i = 0; i < n_threads; i++) {

		data[i].max_row = max_row;
		data[i].max_column = max_column;
		data[i].max_n = max_n;
		data[i].mat = mat;
		data[i].ini_row = i * max_row / n_threads;
		data[i].fin_row = (i + 1) * max_row / n_threads;

		pthread_create(
			&threads[i],
			NULL,
			mandel_thread,
			&data[i]
		);
	}

	for (int i = 0; i < n_threads; i++) {
		pthread_join(threads[i], NULL);	
	}

	//for(int r = 0; r < max_row; ++r){
	//	for(int c = 0; c < max_column; ++c)
	//		std::cout << mat[r][c];
	//	cout << '\n';
	//}	

	free(block);
	free(mat);
}


