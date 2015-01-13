#include <iostream>
#include <fstream>
#include <iomanip>
#include <cmath>
#include <list>
#include <vector>
#include <algorithm>
#include <stdexcept>


size_t get_cnt_lines(const std::string &name_file)
{
	return 0;
}

size_t get_filesize(const std::string & name_file)
{
    std::ifstream in(name_file, std::ifstream::ate | std::ifstream::binary);
    if (!in.is_open())
    {
    	throw std::runtime_error ("get_filesize() can not open file");
    }
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

template <typename T>
void safe_delete(T * &ptr)
{
	if (ptr!=NULL)
	{
		delete[] ptr;
		ptr=NULL;
	}
}

template <typename T>
class Comparator_pos
{
	public:
	const T* scores; 
	Comparator_pos(const T*  _scores ):scores(_scores){}
	bool operator()(size_t a, size_t b) const
	{
		return scores[a]<scores[b];
	}
};

template <typename T>
class Score
{
	public:
		size_t id;
		T score;
		Score(size_t _id, T _score):id(_id),score(_score){}
};


template<typename T>
class Sparse
{
public:
	T* data;
	T * cache_norm;
	size_t * row_ptr;
	size_t * col_ind;
	size_t cnt_nnz;
	size_t dim_x;
	size_t dim_y;
	Sparse():data(NULL),cache_norm(NULL),row_ptr(NULL),col_ind(NULL)
	{}
	~Sparse()
	{
		safe_delete(data);
		safe_delete(cache_norm);
		safe_delete(row_ptr);
		safe_delete(col_ind);
	}
	void print()
	{
		std::cout<<dim_x<<" x " <<dim_y << " sparse matrix\n";
		std::cout<<" with " <<cnt_nnz<< " nonzero elements\n";
		std::cout<<" [";
		for (size_t i = 0; i<10; i++)
			std::cout<<std::fixed << std::setprecision(4) << data[i]<<" ";
//			std::cout<<std::fixed << std::setprecision(4) << col_ind[i]<<" ";
		std::cout<<" ...]\n";
	}
	void prefetch_norm()
	{
		size_t i;
		cache_norm = new T[dim_y];
		for (i = 0; i < dim_y; i++)
		{
			T norm = 0;
			for (size_t x=row_ptr[i]; x<row_ptr[i+1]; x++)
				norm+=data[x]*data[x];
			cache_norm[i] = sqrt(norm);
		}
	}
	void load(std::string path)
	{
		cnt_nnz=load_from_raw(path+"bigrams.data.bin",data);
		cnt_nnz=load_from_raw(path+"bigrams.col_ind.bin",col_ind);
		dim_x = load_from_raw(path+"bigrams.row_ptr.bin",row_ptr)-1;
		dim_y = dim_x;
		prefetch_norm();
	}
	inline T dotproduct_rows(size_t u, size_t v) const
	{
		size_t pos_u=row_ptr[u];
		size_t pos_v=row_ptr[v];
		T result=0;
		while (true)
		{
			if (pos_u>=row_ptr[u+1]) break;
			if (pos_v>=row_ptr[v+1]) break;
			if (col_ind[pos_u]==col_ind[pos_v])
			{
				result+=data[pos_u]*data[pos_v];
				pos_v++;
				pos_u++;
				continue;
			}
			if (col_ind[pos_u]<col_ind[pos_v])
			{
				pos_u++;
				continue;
			}
			if (col_ind[pos_v]<col_ind[pos_u])
			{
				pos_v++;
				continue;
			}
		}
		return result;
	}
	inline T cosine_distance(size_t u, size_t v) const
	{
		return (dotproduct_rows(u,v))/(cache_norm[u]*cache_norm[v]);
	}
	
	template<size_t cnt_rows>
	std::list<Score<T>> get_most_similar_rows(size_t u)
	{
		T * scores = new T[dim_y];
		size_t * positions = new size_t[dim_x];
		for (size_t i=0; i<dim_y; i++)
		{
			positions[i]=i;
			if (i!=u)
			{
				scores[i]=cosine_distance(u,i);
			}
			else
			{
				scores[i]=0;
			}
		}
		Comparator_pos<T> cmp(scores);
		std::sort(positions, positions+dim_x,cmp);
		std::list<Score<T>> result;
		for (size_t i = 0; i< cnt_rows; i++)
		{
			if (i>=dim_y) break;
			size_t id = positions[dim_y-i-1];
			if (scores[id]>0)
				result.push_back(Score<T>(id,scores[id]));
		}

		delete [] scores;
		delete [] positions;
		return result;		
	}
};

void load_word_ids()
{
	std::ifstream in("/storage/scratch/small_bin/ids");
	if (!in.is_open()) {std::cerr<<"can not open file\n";}
}

int main(int argc, char* argv[])
{
	std::string dir_root="/storage/scratch/small_bin/";
	if (argc>1)
		dir_root = std::string(argv[1]);
	std::cerr<<"opening "<<dir_root<<"\n";
	Sparse<float> m;
	m.load(dir_root);
	m.print();
	int i = 1;
	int j = 4;
	std::cerr << "norm of row "<< i << " = " << m.cache_norm[i] << "\n";
	std::cerr << "dotproduct of rows "<< i <<" and " << j << " = " << m.dotproduct_rows(i,j)<<"\n";
	std::cerr << "cosine distance between rows "<< i <<" and " << j << " = " << m.cosine_distance(i,j)<<"\n";
	auto most_similar= m.get_most_similar_rows<10>(i);
	std::cerr << "most similar rows to "<< i <<" are: \n";
	for (auto i: most_similar)
    	std::cout << i.id <<" - " <<i.score<<"\n";
    //load dictionary of words
	return 0;
}