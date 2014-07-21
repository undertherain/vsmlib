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

inline void accumulate(Accumulator & ac,std::string w)
{
    if (ac.find( w ) != ac.end())
        ac[w]++;
    else
        ac.insert(std::make_pair(w,1));
}

void process_sentence(std::string const & s)
{
    boost::char_separator<char> sep(" .,:;!?()[]\t\"'");
    boost::tokenizer<boost::char_separator<char> > tokens(s, sep);
    
    for (const auto& t : tokens) {
        std::string str = t;
        trim3(str);
        accumulate(counters,str);
    }
}

void dump_stat(std::string const & dir_out, Accumulator & ac)
{
    boost::filesystem::path path_full = boost::filesystem::path(dir_out) / boost::filesystem::path("frequencies");
    std::string str_path=path_full.string();

    std::ofstream file;
    file.open (str_path);
    if(!file)
    {
        throw  std::runtime_error("can not open output file "+str_path+" , check the path");
    }
    for (auto t: counters)
    file<<t.first<<"\t"<<t.second<<"\n";
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

    std::string path_out(argv[2]);
    std::ifstream d_file(argv[1]);
    if (!d_file.is_open()) throw std::runtime_error("can not open corpus file");
    std::string line;
    while (std::getline(d_file, line)) 
    {
        process_sentence(line);
    }

    dump_stat(path_out,counters);

    for (const auto& t : counters) 
    {
    }
	return 0;
}
