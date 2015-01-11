#include <iostream>
#include <fstream>
#include <iomanip>

size_t get_cnt_lines(const std::string &name_file)
{
	return 0;
}

size_t get_filesize(const std::string & name_file)
{
    std::ifstream in(name_file, std::ifstream::ate | std::ifstream::binary);
    return in.tellg(); 
}

template <typename T>
size_t load_from_raw(std::string name_file,T*&buffer)
{
	size_t size_file = get_filesize(name_file);
	size_t cnt_items = size_file / sizeof(T);
//	std::cerr<<"size file = " << size_file << "\n";
//	std::cerr<<"cnt elements = " << cnt_items << "\n";
	buffer = new T[cnt_items];
    std::ifstream is(name_file, std::ifstream::in | std::ifstream::binary);
   	is.read(reinterpret_cast<char *>(buffer),size_file);
   	return cnt_items;
}

template<typename T>
class Sparse
{
public:
	T* data;
	size_t * row_ptr;
	size_t * col_ind;
	size_t cnt_nnz;
	size_t dim_x;
	size_t dim_y;
	void print()
	{
		std::cout<<dim_x<<" x " <<dim_y << " sparse matrix\n";
		std::cout<<"[";
		for (size_t i = 0; i<10; i++)
//			std::cout<<std::fixed << std::setprecision(4) << data[i]<<" ";
			std::cout<<std::fixed << std::setprecision(4) << col_ind[i]<<" ";
		std::cout<<" ...]\n";
	}
	void load(std::string path)
	{
		cnt_nnz=load_from_raw(path+"bigrams.data.bin",data);
		cnt_nnz=load_from_raw(path+"bigrams.col_ind.bin",col_ind);
		dim_x = load_from_raw(path+"bigrams.row_ptr.bin",row_ptr);
		dim_y = dim_x;
	}
};


int main(int argc, char* argv[])
{
	std::cout<<"Heelo sparse\n";
	Sparse<float> m;
	m.load("/storage/scratch/small_bin/");
	m.print();
	return 0;
}