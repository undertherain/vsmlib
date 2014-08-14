#include <iostream>
#include <string>
#include <cstring>
#include <fstream>
#include <set>
#include <map>
#include <exception>
#include <algorithm>
#include <boost/filesystem.hpp>
#include <boost/property_tree/xml_parser.hpp>
#include <boost/property_tree/ptree.hpp>
#include <boost/foreach.hpp>
#include <boost/tokenizer.hpp>
#include "string_tools.hpp"
#include "basic_utils/buffer_byte.hpp"


unsigned long long cnt_words;
typedef std::map<std::string,unsigned long> Accumulator;
std::map<std::string,Accumulator> counters;

void accumulate(Accumulator & ac,std::string w)
{
    if (ac.find( w ) != ac.end())
        ac[w]++;
    else
        ac.insert(std::make_pair(w,1));
}

void clean(std::string & str)
{
    for (unsigned int i=0;i<str.length();i++)
        if (str[i]=='/')
            str[i]='_';
}

void process_sentence(std::string const & s)
{
  //  for (unsigned int i=0; i<s.length(); i++)
    //    if (s[i]==' ') cnt_white++;
    return ;
    boost::char_separator<char> sep(" .,:;!?()[]\t'\"");
    boost::tokenizer<boost::char_separator<char> > tokens(s, sep);
    std::string w_prev;
    for (const auto& t : tokens) {
        std::string w_current=t;
        //clean(str_current);
        if (counters.find( w_prev ) != counters.end())
            accumulate(counters[w_prev],w_current);
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

void print_line(const byte * buf) 
{
    for (unsigned long i=0;i<12;i++)
        std::cout<<buf[i];
}

class Comparator
{
    byte * ptr=NULL;
public:
    Comparator (byte * _ptr):ptr(_ptr){}
    bool operator ()(Index r,Index l)
    {
        return std::strcmp(reinterpret_cast<const char *>(ptr+l), reinterpret_cast<const char *>(ptr+r)) > 0;
    }
};


int main(int argc, char * argv[])
{
   if (argc<3)
    {
      std::cerr << "usage: " << argv[0] << " corpus_file output_dir [word]\n";
      return 0;
    } 
    //counters.insert(std::make_pair(std::string(argv[3]),Accumulator()));
    std::string path_out(argv[2]);
    //std::ifstream d_file(argv[1]);
    std::string s="test";
    BufferByte buf_in=BufferByte::LoadFromFile(argv[1]);
   // buf_in.Print();
    Index cnt_white=0;
    for (Index i=0;i<buf_in.size;i++)
    {
        if (buf_in.buffer[i]==' ') cnt_white++;
    }
    std::cout<<cnt_white<<"\t words found\n";
    //Index pos_prev = 0; // todo this should be negative!!!!
    Index pos_current = 0;
    Index * ptr_delimiters=new Index[cnt_white];
    ptr_delimiters[pos_current++]=0;
    std::cerr<<"buf_in.size = "<<buf_in.size<<"\n";
    for (Index i=0;i<buf_in.size;i++)
    {
        if (buf_in.buffer[i]==' ')
        {   
            while (buf_in.buffer[i+1]=='\n') i++;
            ptr_delimiters[pos_current++]=i+1;
        }
    }
    std::sort (ptr_delimiters, ptr_delimiters+pos_current,Comparator(buf_in.buffer));
    for (unsigned long i=0;i<cnt_white;i++)
    {
        Index pos_symbol=0;
        while ((pos_symbol<buf_in.size)){}
        //std::cout<<ptr_delimiters[i]<<"\t";
        //print_line(buf_in.buffer+ptr_delimiters[i]);
        //std::cout<<"\n";
    }

    delete [] ptr_delimiters;
	return 0;
}
