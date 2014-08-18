#include <iostream>
#include <string>
#include <cstring>
#include <fstream>
#include <sstream>
#include <exception>
#include <cstring>
#include <boost/tokenizer.hpp>
#include <boost/filesystem.hpp>
#include <map>
#include <unordered_map>

std::ofstream file;
typedef unsigned long Index;

#include "string_tools.hpp"
#include "ternary_tree.hpp"
TernaryTreeNode<Index> * tree_ids=NULL;


unsigned long long cnt_words;
typedef std::map<Index,Index> Accumulator;
std::map<Index,Accumulator> counters;

template <typename T>
    std::string ConvertToStr(const T & val)
    {
        std::ostringstream out;
        out << val;
        std::string str = out.str();
        return str;
    }

inline void accumulate_ids(const std::string & w)
{
        set_id<Index>(tree_ids,w.c_str());
}


void accumulate(Accumulator & ac,Index w)
{
    if (ac.find( w ) != ac.end())
        ac[w]++;
    else
        ac.insert(std::make_pair(w,1));
}

void accumulate(Index first, Index second)
{
    //if (second.length()<2) return;
    if (counters.find( first ) == counters.end())
        counters.insert(std::make_pair(first,Accumulator()));
    accumulate(counters[first],second);
}


void process_sentence_ids(std::string const & s)
{
    boost::char_separator<char> sep(" .,:;!?()[]\t\"'");
    boost::tokenizer<boost::char_separator<char> > tokens(s, sep);
    for (const auto& t : tokens) {
        std::string str = t;
        trim3(str);
        accumulate_ids(str);
    }
}


void process_sentence(std::string const & s)
{
    boost::char_separator<char> sep(" .,:;!?()[]\t'\"");
    boost::tokenizer<boost::char_separator<char> > tokens(s, sep);
    std::string w_prev;
    for (const auto& t : tokens) {
        std::string w_current=t;
        //clean(str_current);
       // if (counters.find( w_prev ) != counters.end())
        if (w_prev.length()>1)
//            accumulate(counters[w_prev],w_current);
            accumulate(get_value(tree_ids,w_prev.c_str()),get_value(tree_ids,w_current.c_str()));
        //std::cerr<<"w_prev = "<<w_prev<<" , w_current = "<<w_current<<"\n";
//        if (w_prev.length()!=0)
        //if (counters.find( w_current ) != counters.end())
//            accumulate(counters[w_current],std::string("-")+w_prev);
//            accumulate(counters[w_current],w_prev);
//        std::cout << w_prev<<" " << t << std::endl;
        w_prev=w_current;
    }
}




int main(int argc, char * argv[])
{
   if (argc<3)
    {
      std::cerr << "usage: " << argv[0] << " corpus_file output_dir \n";
      return 0;
    }
    tree_ids = new TernaryTreeNode<unsigned long>();
    tree_ids->c='m';

    std::string path_out(argv[2]);
    std::ifstream d_file(argv[1]);
    if (!d_file.is_open()) throw std::runtime_error("can not open corpus file");
    
    std::string line;
    while (std::getline(d_file, line)) 
    {
        process_sentence_ids(line);
    }

    d_file.clear();
    d_file.seekg(std::ios_base::beg);
    
    while (std::getline(d_file, line)) 
    {
        process_sentence(line);
    }
    //dump ids

    boost::filesystem::path path_full = boost::filesystem::path(path_out) / boost::filesystem::path("ids");
    std::string str_path=path_full.string();
    file.open (str_path);
    if(!file)
    {
        throw  std::runtime_error("can not open output file "+str_path+" , check the path");
    }
    traverse<Index>(tree_ids,0);
    file.close();

    //end dump ids

    path_full = boost::filesystem::path(path_out) / boost::filesystem::path("bigrams_list");
    str_path=path_full.string();
    file.open (str_path);
    if(!file)
    {
        throw  std::runtime_error("can not open output file "+str_path+" , check the path");
    }

    for (const auto& first : counters) 
    {
        //dump_stat(first.first,path_out,t.second);
        for (const auto& second : first.second) 
        {
            //if (t.second>0)
            file<<first.first-1<<"\t"<<second.first-1<<"\t"<<second.second<<"\n";
        }

    }

    file.close();



    return 0;
}