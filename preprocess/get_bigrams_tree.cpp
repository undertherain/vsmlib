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
#include <unordered_map>

typedef unsigned long Index;

#include "string_tools.hpp"
#include "ternary_tree.hpp"
TernaryTreeNode<Index> * tree=NULL;
//TernaryTreeNode<Index> * tree_freq=NULL;


unsigned long long cnt_words;
typedef std::map<Index,Index> Accumulator;
std::map<Index,Accumulator> counters;
std::vector<Index> freq_per_id;

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
        if (str.length()<2) continue;
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
    boost::char_separator<char> sep(" .,:;!?()[]\t'\"");
    boost::tokenizer<boost::char_separator<char> > tokens(s, sep);
    std::string w_prev;
    for (const auto& t : tokens) {
        std::string w_current=t;
        trim3(w_current);
        if (w_current.length()<2) continue;
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
//        if (w_prev.length()!=0)
        //if (counters.find( w_current ) != counters.end())
//            accumulate(counters[w_current],std::string("-")+w_prev);
//            accumulate(counters[w_current],w_prev);
//        std::cout << w_prev<<" " << t << std::endl;
        w_prev=w_current;
    }
}

void write_value_to_file(std::string name,Index value)
{
    std::ofstream file(name);
    file<<value;
    file.close();
}

void write_vector_to_file(std::string name,std::vector<Index> const &  values)
{
    std::ofstream file(name);
    for (Index i=0;i<values.size();i++)
        file<<i<<"\t"<<values[i]<<"\n";
    file.close();
}

void dump_crs(std::string path_out)
{
    std::ofstream file;
    std::string str_path = (boost::filesystem::path(path_out) / boost::filesystem::path("bigrams.data")).string();
    file.open (str_path);
    if(!file) throw  std::runtime_error("can not open output file "+str_path+" , check the path");
    for (const auto& first : counters)  //vriting data
    {
        for (const auto& second : first.second) 
        {
            double v=log2((static_cast<double>(second.second)*cnt_words)/(freq_per_id[first.first]*freq_per_id[second.first]));
            file<<v<<"\n";
        }
    }
    file.close();
    str_path = (boost::filesystem::path(path_out) / boost::filesystem::path("bigrams.col_ind")).string();
    file.open (str_path);
    for (const auto& first : counters)  //vriting columnt indices
    {
        for (const auto& second : first.second) 
        {
            file<<second.first<<"\n";
        }
    }
    file.close();
    str_path = (boost::filesystem::path(path_out) / boost::filesystem::path("bigrams.row_ptr")).string();
    file.open (str_path);
    Index row_ptr=0;
    Index id_last=0;
    for (const auto& first : counters)  //vriting columnt indices
    {
        std::cerr<<"first.first = "<<first.first<<"\t count = "<<first.second.size()<<"\n";
        if (first.first==0) file<<row_ptr<<"\n";
        else
            for (Index k=id_last;k<first.first;k++)
                file<<row_ptr<<"\n";
            id_last=first.first;
            row_ptr+=first.second.size();
    }
    for (Index k=id_last;k<id_global;k++)
         file<<row_ptr<<"\n";

    file.close();
}

int main(int argc, char * argv[])
{
   if (argc<3)
    {
      std::cerr << "usage: " << argv[0] << " corpus_file output_dir \n";
      return 0;
    }
    tree = new TernaryTreeNode<unsigned long>();
    tree->c='m';
/*
    set_id_and_increment(tree,"cat");
    set_id_and_increment(tree,"cax");
    set_id_and_increment(tree,"banana");
    //set_id_and_increment(tree,"applx");
    std::cerr <<"frequencies:\n";
    dump_frequency(std::cerr, tree,0);
    std::cerr <<"ids:\n";
    dump_ids(std::cerr, tree,0);
    get_id(tree,"cat");
    get_id(tree,"cax");
    get_id(tree,"banana");
  */  
//    return 0;

    std::string path_out(argv[2]);
    std::ifstream d_file(argv[1]);
    if (!d_file.is_open()) throw std::runtime_error("can not open corpus file");
    
    std::cerr<<"assigning ids\n";
    std::string line;
    while (std::getline(d_file, line)) 
    {
        process_sentence_ids(line);
    }
    boost::filesystem::path path_full = boost::filesystem::path(path_out) / boost::filesystem::path("ids");
    std::string str_path=path_full.string();
    std::ofstream file;
    file.open (str_path);
    if(!file)  throw  std::runtime_error("can not open output file "+str_path+" , check the path");
    dump_ids<Index>(file,tree,0);
    file.close();

    path_full = boost::filesystem::path(path_out) / boost::filesystem::path("frequencies");
    str_path=path_full.string();
    file.open (str_path);
    if(!file)  throw  std::runtime_error("can not open output file "+str_path+" , check the path");
    dump_frequency<Index>(file,tree,0);
    file.close();

    write_value_to_file((boost::filesystem::path(path_out) / boost::filesystem::path("cnt_unique_words")).string(),id_global);
    write_value_to_file((boost::filesystem::path(path_out) / boost::filesystem::path("cnt_words")).string(),cnt_words);
    write_vector_to_file((boost::filesystem::path(path_out) / boost::filesystem::path("freq_per_id")).string(),freq_per_id);
    //end dump ids

    std::cerr<<"extracting bigrams\n";
    d_file.clear();
    d_file.seekg(std::ios_base::beg);
    
    while (std::getline(d_file, line)) 
    {
        process_sentence(line);
    }

    
    path_full = boost::filesystem::path(path_out) / boost::filesystem::path("bigrams_list");
    str_path=path_full.string();
    file.open (str_path);
    if(!file) throw  std::runtime_error("can not open output file "+str_path+" , check the path");
    for (const auto& first : counters) 
    {
        for (const auto& second : first.second) 
        {
            //if (t.second>0)
//            file<<first.first<<"\t"<<second.first<<"\t"<<second.second<<"\n";
            double v=log2((static_cast<double>(second.second)*cnt_words)/(freq_per_id[first.first]*freq_per_id[second.first]));
            file<<first.first<<"\t"<<second.first<<"\t"<<v<<"\n";
        }

    }

    file.close();
    dump_crs(path_out);
    return 0;
}