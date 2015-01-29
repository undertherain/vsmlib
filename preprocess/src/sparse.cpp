#include <iostream>
#include <fstream>
#include <iomanip>
#include <cmath>
#include <list>
#include <vector>
#include <unordered_map>
#include <algorithm>
#include <stdexcept>
#include <boost/tokenizer.hpp>
#include <boost/filesystem.hpp>
#include "string_tools.hpp"
#include <cassert>

std::unordered_map<std::string,size_t> dic_words;
std::vector<std::string> words;
int64_t * frequencies;

size_t get_cnt_lines(const std::string &name_file)
{
	return 0;
}

size_t get_filesize(const std::string & name_file)
{
    std::ifstream in(name_file, std::ifstream::ate | std::ifstream::binary);
    if (!in.is_open())
    {
    	std::string message="get_filesize() can not open file ";
    	throw std::runtime_error (message+name_file);
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
		std::cout<<" words_of_interesth " <<cnt_nnz<< " nonzero elements\n";
		std::cout<<" [";
		for (size_t i = 0; i<10; i++)
			std::cout<<std::fixed << std::setprecision(4) << data[i]<<" ";
//			std::cout<<std::fixed << std::setprecision(4) << col_ind[i]<<" ";
		std::cout<<" ...]\n";
	}
	void prefetch_norm()
	{
		std::cerr<<"prefetching norm \n";
		size_t i;
		cache_norm = new T[dim_y];
		for (i = 0; i < dim_y; i++)
		{
			T norm = 0;
			for (size_t x=row_ptr[i]; x<row_ptr[i+1]; x++)
				norm+=data[x]*data[x];
			cache_norm[i] = sqrt(norm);
		}
		std::cerr<<"done \n";
	}
	void load(std::string path)
	{
		std::cerr<<"loading bigrams \n";
		cnt_nnz=load_from_raw(path+"bigrams.data.bin",data);
		std::cerr<<"loading col_ind \n";
		cnt_nnz=load_from_raw(path+"bigrams.col_ind.bin",col_ind);
		std::cerr<<"loading row_ptr \n";
		dim_x = load_from_raw(path+"bigrams.row_ptr.bin",row_ptr);
		dim_y = dim_x;
		std::cerr<<"dim y = "<<dim_y<<"\n";
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
		if ((cache_norm[u]==0) || (cache_norm[v]==0)) return 0;
		return (dotproduct_rows(u,v))/(cache_norm[u]*cache_norm[v]);
	}
	
	template<size_t cnt_rows>
	std::list<Score<T>> get_most_similar_rows(size_t u)
	{
		if ((u<0)||(u>=dim_y)) {throw std::runtime_error("word index out of range in get similar vectors");}
		T * scores = new T[dim_y];
		size_t * positions = new size_t[dim_y];
		#pragma omp parallel for
		for (size_t i=0; i<dim_y; i++)
		{
			positions[i]=i;
			if (i!=u)
			{
				scores[i]=cosine_distance(u,i) * log(0.1+frequencies[i]);
			}
			else
			{
				scores[i]=0;
			}
		}
		std::sort(positions, positions+dim_y,Comparator_pos<T>(scores));
		std::list<Score<T>> result;
		size_t cnt = cnt_rows;
		if (cnt>dim_y) cnt = dim_y;
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
	
	template<size_t cnt_rows>
	std::list<Score<T>> get_most_similar_rows(std::string key)
	{
		if (dic_words.count(key)==0) 
		{
			std::list<Score<T>> empty;
			return empty;
		}
		return get_most_similar_rows<cnt_rows>(dic_words[key]);		
	}
	void report_most_similar(std::string query)
	{
		auto most_similar= get_most_similar_rows<10>(query);
		std::cout << "\nmost similar rows to *"<< query <<"* ["<<frequencies[dic_words[query]]<<"] are: \n";
		for (auto i: most_similar)
    	std::cout << "\t" <<i.id<<" - " <<words[i.id] <<" ["<<frequencies[i.id]<<"] - " <<i.score<<"\n";
	}	
};

void load_word_ids(boost::filesystem::path dir_root)
{
	std::ifstream in((dir_root / boost::filesystem::path("ids")).string());
	if (!in.is_open()) {std::cerr<<"can not open file\n";}
	std::string line;
    boost::char_separator<char> sep("\t");
	while( std::getline( in, line ) ) 
	{
    	boost::tokenizer<boost::char_separator<char> > tokens(line, sep);
        auto beg=tokens.begin();
        std::string key=*beg;
        beg++;
        std::string svalue=*beg;
        size_t value = stoull (svalue);
        dic_words.insert(std::pair<std::string,size_t>(key,value));
        words[value]=key;
    }
    in.close();
}
size_t load_frequencies(boost::filesystem::path dir_root)
{
	std::cerr<<"loading frequencies";
	 auto cnt_freq =  load_from_raw((dir_root / boost::filesystem::path("freq_per_id")).string(),frequencies);
	 return  cnt_freq;
/*
	std::ifstream in((dir_root / boost::filesystem::path("freq_per_id")).string());
	if (!in.is_open()) {std::cerr<<"can not open file\n";}
	std::string line;
    size_t id = 0;
	while( std::getline( in, line ) ) 
	{
    //	boost::tokenizer<boost::char_separator<char> > tokens(line, sep);
      //  auto beg=tokens.begin();
        //std::string svalue=*beg;
        //size_t id = stoull (svalue);
        //beg++;
        //svalue=*beg;
        size_t value = stoull (line);
        frequencies[id++]=value;
    }
    in.close();
    */
}

int main(int argc, char* argv[])
{
	std::string dir_root="/storage/scratch/small_bin/";
	if (argc>1)
		dir_root = std::string(argv[1]);
	std::cout<<"opening "<<dir_root<<"\n";
	Sparse<float> m;
	m.load(dir_root);
	m.print();
    words.resize(m.dim_y+1);
    //frequencies.resize(m.dim_y);
	//std::cerr<<"loading word ids\n";
	load_word_ids(dir_root);
	//std::cerr<<"done\n";
	auto cnt_f = load_frequencies(dir_root);
	std::cerr<<"loaded " <<cnt_f<<" frequencies\n";
	//int i = 0;
	//int j = 4;
	
	//std::cerr << "norm of row "<< i << " = " << m.cache_norm[i] << "\n";
	//std::cerr << "dotproduct of rows "<< i <<" and " << j << " = " << m.dotproduct_rows(i,j)<<"\n";
	//std::cerr << "cosine distance between rows "<< i <<" and " << j << " = " << m.cosine_distance(i,j)<<"\n";
	//auto most_similar= m.get_most_similar_rows<10>(i);
	auto wordlist=load_words("words_of_interest.txt");
	for (auto i: wordlist)
		m.report_most_similar(i);
		
	return 0;
}
