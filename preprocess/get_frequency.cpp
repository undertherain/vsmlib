#include <iostream>
#include <string>
#include <cstring>
#include <fstream>
#include <set>
#include <unordered_set>
#include <map>
#include <exception>
#include <boost/filesystem.hpp>
#include <boost/property_tree/xml_parser.hpp>
#include <boost/property_tree/ptree.hpp>
#include <boost/foreach.hpp>
#include <boost/tokenizer.hpp>
#include "string_tools.hpp"
using boost::property_tree::ptree;

unsigned long long cnt_words;
typedef std::map<std::string,unsigned long> Accumulator;

std::unordered_set<std::string> keys;
Accumulator counters;

void load_words()
{
	std::ifstream d_file("words_of_interest.txt");
    std::string line;
    while( std::getline( d_file, line ) ) 
    {
        trim3(line);
        counters.insert(std::make_pair(line,0));
        keys.insert(line);
    }
}

inline void accumulate(Accumulator & ac,std::string w)
{
//    if (ac.find( w ) != ac.end())
      ac[w]++;
//    else
//        ac.insert(std::make_pair(w,1));
}

void process_sentence(std::string const & s)
{
    boost::char_separator<char> sep(", ");
    boost::tokenizer<boost::char_separator<char> > tokens(s, sep);
    std::string w_prev;
    for (const auto& t : tokens) {
        if (keys.find(t) != keys.end())
        //if (counters.find(t) != counters.end())
            accumulate(counters,t);
    }
}

void dump_stat(std::string const & name,std::string const & dir_out, Accumulator & ac)
{
    boost::filesystem::path path_full = boost::filesystem::path(dir_out) / boost::filesystem::path(name);
    std::string str_path=path_full.string();

    std::ofstream file;
    file.open (str_path);
    if(!file)
    {
        throw  std::runtime_error("can not open output file "+str_path+" , check the path");
    }
    unsigned long  tmp=ac[name];
    file<<tmp;
    //file<<"\n";
    file.close();
}

int main(int argc, char * argv[])
{
   if (argc<3)
    {
      std::cerr << "usage: " << argv[0] << " corpus_file output_dir [word]\n";
      return 0;
    }

    if (argc<4)  
        load_words();
    else
        counters.insert(std::make_pair(std::string(argv[3]),0));

    std::string path_out(argv[2]);
    std::ifstream d_file(argv[1]);
    if (!d_file.is_open()) throw std::runtime_error("can not open corpus file");
    std::string line;
    while (std::getline(d_file, line)) 
    {
        process_sentence(line);
    }
    for (const auto& t : counters) 
    {
        dump_stat(t.first,path_out,counters);
    }
	return 0;
}
