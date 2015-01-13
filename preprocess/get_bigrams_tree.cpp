#include <iostream>
#include <string>
#include <cstring>
#include <cmath>
#include <fstream>
#include <sstream>
#include <exception>
#include <cstring>
#include <boost/tokenizer.hpp>
#include <boost/filesystem.hpp>
#include <map>
#include <set>
#include <unordered_map>
#include <cstdarg>

typedef unsigned long Index;

#include "string_tools.hpp"
#include "ternary_tree.hpp"
TernaryTreeNode<Index> * tree=NULL;
//TernaryTreeNode<Index> * tree_freq=NULL;


Index cnt_words;
Index cnt_words_processed;
Index cnt_bigrams;
Index current_max;
typedef std::map<Index,Index> Accumulator;
std::map<Index,Accumulator> counters;
std::vector<Index> freq_per_id;

#include "basic_utils/write_data.hpp"

template <typename T>
std::string ConvertToStr(const T & val)
{
    std::ostringstream out;
    out << val;
    std::string str = out.str();
    return str;
}

void accumulate(Accumulator & ac,Index w)
{
    if (ac.find( w ) != ac.end())
        ac[w]++;
    else
    {
        ac.insert(std::make_pair(w,1));
        cnt_bigrams++;
    }
}

void accumulate(Index first, Index second)
{
    //if (second.length()<2) return;
    if (counters.find( first ) == counters.end())
        counters.insert(std::make_pair(first,Accumulator()));
    accumulate(counters[first],second);
}

const char * separators=" .,:;!?()[]\t\"'";

void process_sentence_ids(std::string const & s)
{
    boost::char_separator<char> sep(separators);
    boost::tokenizer<boost::char_separator<char> > tokens(s, sep);
    for (const auto& t : tokens) {
        std::string str = t;
        clean(str);
        if (!is_word_valid(str)) continue;
        cnt_words++;
        Index i=set_id_and_increment(tree,str.c_str());
        if (freq_per_id.size()<i+1) freq_per_id.push_back(0);
        freq_per_id[i]++;
        //increment<Index>(tree_freq,str.c_str());
    }
}


void process_sentence(std::string const & s)
{
 if (s.length()<2) return;
 boost::char_separator<char> sep(separators);
 boost::tokenizer<boost::char_separator<char> > tokens(s, sep);
 std::string w_prev;
 for (const auto& t : tokens) {
    std::string w_current=t;
    clean(w_current);
    if (!is_word_valid(w_current)) continue;

    cnt_words_processed++;
    if (current_max<get_id(tree,w_current.c_str()))
         current_max=get_id(tree,w_current.c_str());

        //clean(str_current);
       // if (counters.find( w_prev ) != counters.end())
//            accumulate(counters[w_prev],w_current);
    if (w_prev.length()>1)
    {
            //if get_id(tree,w_prev.c_str())
        accumulate(get_id(tree,w_prev.c_str()),get_id(tree,w_current.c_str()));
            //std::cerr<<w_prev<<"\t"<<w_current<<'\n';
    }
        //std::cerr<<"w_prev = "<<w_prev<<" , w_current = "<<w_current<<"\n";
    //if (w_prev.length()!=0)
        //accumulate( get_id(tree,w_current.c_str()),get_id(tree,w_prev.c_str()    ) ) ;
//    
  //if (counters.find( w_current ) != counters.end())
//            accumulate(counters[w_current],std::string("-")+w_prev);
          //std::cout << w_prev<<" " << t << std::endl;
    w_prev=w_current;
}
}


class DirReader
   {
    //std::string dir;
    boost::filesystem::recursive_directory_iterator dir,initial;
    std::ifstream file_in;
public:
    DirReader(std::string _dir):dir(_dir),initial(_dir)
    {
        file_in.open(dir->path().string());
        std::cerr<<"processing \t"<<dir->path().string()<<'\n';
        //reset();
    }
    void reset()
    {
        dir=initial;
        if (file_in.is_open()) file_in.close();
        file_in.open(dir->path().string());
        std::cerr<<"processing \t"<<dir->path().string()<<'\n';
    }
    bool getline(std::string & line)
    {
        boost::filesystem::recursive_directory_iterator end;
        if (!file_in.eof())
        {
            std::getline(file_in, line);
            return true;
        } else 
        {
            dir++;
            if (dir==end)
            {
                file_in.close();
                return false;
            }
            else 
            {
                std::cerr<<"processing \t"<<dir->path().string()<<'\n';
                file_in.close();
                file_in.open(dir->path().string());
                std::getline(file_in, line);
                return true;
            }
        }
    }
};

int main(int argc, char * argv[])
{
 if (argc<3)
 {
  std::cerr << "usage: " << argv[0] << " corpus_dir output_dir \n";
  return 0;
}
load_stopwords();

tree = new TernaryTreeNode<unsigned long>();
tree->c='m';

boost::filesystem::path path_out(argv[2]);
write_values_to_file((path_out / boost::filesystem::path("cnt_bigrams")).string(),"cnt_words","cnt_unique_words","cnt_bigrams");

std::cerr<<"assigning ids\n";
DirReader dr(argv[1]);
std::string line;
while (dr.getline(line) )
{
    process_sentence_ids(line);
}
std::ofstream file;
file.open ((path_out / boost::filesystem::path("ids")).string());
    //if(!file)  throw  std::runtime_error("can not open output file "+str_path+" , check the path");
dump_ids<Index>(file,tree,0);
file.close();

std::string str_path=(path_out / boost::filesystem::path("frequencies")).string();
file.open (str_path);
if(!file)  throw  std::runtime_error("can not open output file "+str_path+" , check the path");
dump_frequency<Index>(file,tree,0);
file.close();

write_value_to_file((path_out / boost::filesystem::path("cnt_unique_words")).string(),id_global);
write_value_to_file((path_out / boost::filesystem::path("cnt_words")).string(),cnt_words);
write_vector_to_file((path_out / boost::filesystem::path("freq_per_id")).string(),freq_per_id);

std::cerr<<"extracting bigrams\n";
dr.reset();
Index cnt_words_last_dump=0;
        append_values_to_file((boost::filesystem::path(path_out) / boost::filesystem::path("cnt_bigrams")).string(),0,0,0);
while (dr.getline(line) )
{
    process_sentence(line);
    if (cnt_words_processed-cnt_words_last_dump>50000)
    {
        append_values_to_file((boost::filesystem::path(path_out) / boost::filesystem::path("cnt_bigrams")).string(),cnt_words_processed,current_max+1,cnt_bigrams);
        cnt_words_last_dump=cnt_words_processed;
    }
}

std::cerr<<"dumping results to disk\n";

str_path=(path_out / boost::filesystem::path("bigrams_list")).string();
file.open (str_path);
if(!file) throw  std::runtime_error("can not open output file "+str_path+" , check the path");
//Index cnt_bigrams=0;
for (const auto& first : counters) 
{
    for (const auto& second : first.second) 
    {
//      if (t.second>0)
//      file<<first.first<<"\t"<<second.first<<"\t"<<second.second<<"\n";
        double v=log2((static_cast<double>(second.second)*cnt_words)/(freq_per_id[first.first]*freq_per_id[second.first]));
        file<<first.first<<"\t"<<second.first<<"\t"<<v<<"\n";
  //      cnt_bigrams++;
    }
}
file.close();
//dump_crs(path_out.string());
dump_crs_bin(path_out.string());
return 0;
}