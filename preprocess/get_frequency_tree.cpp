#include <iostream>
#include <string>
#include <cstring>
#include <fstream>
#include <exception>
#include <cstring>
#include <boost/tokenizer.hpp>
#include <boost/filesystem.hpp>

std::ofstream file;
typedef unsigned long Index;

#include "string_tools.hpp"
#include "ternary_tree.hpp"
TernaryTreeNode<Index> * tree=NULL;
TernaryTreeNode<Index> * tree_ids=NULL;


inline void accumulate(const std::string & w)
{
    increment<Index>(tree,w.c_str());
//    set_id<Index>(tree,w.c_str());
}

void process_sentence(std::string const & s)
{
    boost::char_separator<char> sep(" .,:;!?()[]\t\"'");
    boost::tokenizer<boost::char_separator<char> > tokens(s, sep);
    for (const auto& t : tokens) {
        std::string str = t;
        trim3(str);
        accumulate(str);
    }
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

    std::string path_out(argv[2]);
    std::ifstream d_file(argv[1]);
    if (!d_file.is_open()) throw std::runtime_error("can not open corpus file");
    
    std::string line;
    while (std::getline(d_file, line)) 
    {
        process_sentence(line);
    }
    //std::cerr <<"apple = "<<get_value<unsigned long>(tree,"apps")<<"\n";
    boost::filesystem::path path_full = boost::filesystem::path(path_out) / boost::filesystem::path("frequencies");
    std::string str_path=path_full.string();
    file.open (str_path);
    if(!file)
    {
        throw  std::runtime_error("can not open output file "+str_path+" , check the path");
    }
    traverse<Index>(tree,0);
    file.close();
 //   dump_stat(path_out,counters);
    return 0;
}