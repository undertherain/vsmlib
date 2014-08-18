#include <iostream>
#include <string>
#include <cstring>
#include <fstream>
#include <set>
#include <map>
#include <exception>
#include <boost/filesystem.hpp>
#include <boost/property_tree/xml_parser.hpp>
#include <boost/property_tree/ptree.hpp>
#include <boost/foreach.hpp>
#include <boost/tokenizer.hpp>
#include "string_tools.hpp"
//using boost::property_tree::ptree;

unsigned long long cnt_words;
typedef std::map<std::string,unsigned long> Accumulator;
std::map<std::string,Accumulator> counters;


void load_words()
{
	std::ifstream d_file("words_of_interest.txt");
    std::string line;
    while( std::getline( d_file, line ) ) 
    {
        trim3(line);
        counters.insert(std::make_pair(line,Accumulator()));
    }
}

void accumulate(Accumulator & ac,std::string w)
{
    if (ac.find( w ) != ac.end())
        ac[w]++;
    else
        ac.insert(std::make_pair(w,1));
}

void accumulate(std::string first, std::string second)
{
    if (second.length()<2) return;
    if (counters.find( first ) == counters.end())
        counters.insert(std::make_pair(first,Accumulator()));
    accumulate(counters[first],second);
}

void clean(std::string & str)
{
    for (unsigned int i=0;i<str.length();i++)
        if (str[i]=='/')
            str[i]='_';
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
            accumulate(w_prev,w_current);
        //std::cerr<<"w_prev = "<<w_prev<<" , w_current = "<<w_current<<"\n";
        if (w_prev.length()!=0)
        if (counters.find( w_current ) != counters.end())
            accumulate(counters[w_current],std::string("-")+w_prev);
//            accumulate(counters[w_current],w_prev);
//        std::cout << w_prev<<" " << t << std::endl;
        w_prev=w_current;
    }
}

void dump_stat(std::string name,std::string dir_out, Accumulator const & ac)
{
    if (ac.size()==0) return;
    boost::filesystem::path path_full = boost::filesystem::path(dir_out) / boost::filesystem::path(name);
    std::string str_path=path_full.string();

    std::ofstream file;
    //std::cout << "dumping " <<str_path;
    file.open (str_path);

    if(!file)
    {
        throw  std::runtime_error("can not open output file "+str_path+" , check the path");
    }

    for (const auto& t : ac) 
    {
        if (t.second>0)
        file<<t.first<<"\t"<<t.second<<"\n";
    }
    file.close();
}

int main(int argc, char * argv[])
{
   if (argc<3)
    {
      std::cerr << "usage: " << argv[0] << " corpus_file output_dir [word]\n";
      return 0;
    } 
  //  if (argc<4)  
    //    load_words();
    //else
      //  counters.insert(std::make_pair(std::string(argv[3]),Accumulator()));
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
        dump_stat(t.first,path_out,t.second);
    }
	return 0;
}
