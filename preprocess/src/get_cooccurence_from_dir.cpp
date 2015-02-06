#include <iostream>
#include <string>
#include <cstring>
#include <cmath>
#include <fstream>
#include <sstream>
#include <exception>
#include <cstring>
#include <boost/tokenizer.hpp>
#include <boost/circular_buffer.hpp>
#include <boost/filesystem.hpp>
#include <map>
#include <set>
#include <unordered_map>
#include <cstdarg>
#include "options.hpp"

typedef int64_t Index;
std::string provenance;

#include "basic_utils/utils.hpp"
//#include "basic_utils/stream_reader.hpp"
#include "vocabulary.hpp"

Index cnt_words_processed;
Index cnt_bigrams;
typedef std::map<Index,Index> Accumulator;
std::map<Index,Accumulator> counters;
std::vector<Index> freq_per_id;
Vocabulary vocab;
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
    if ((first<0)||(second<0)) return;
    //if (second.length()<2) return;
    if (counters.find( first ) == counters.end())
        counters.insert(std::make_pair(first,Accumulator()));
    accumulate(counters[first],second);
}

void process_sentence(std::string const & s)
{
 if (s.length()<2) return;
// std::cerr<<" line: "<<s<<"\n";
 boost::char_separator<char> sep(separators);
 boost::tokenizer <boost::char_separator<char> > tokens(s, sep);
 //std::string w_prev;
 int64_t id_prev=-1;
for (const auto& t : tokens) {
    std::string w_current=t;
    //std::cerr<<"current word= "<<w_current<<"\n";
    clean(w_current);
    if (!vocab.is_word_valid(w_current))  continue;
    //std::cerr<<"is valid!\n";
    Index id_current=vocab.get_id(w_current.c_str());
    if (id_current<0) continue;
    //std::cerr<<"passed\n";
    freq_per_id[id_current]++;
    cnt_words_processed++;
   // if (current_max<id_current) current_max=id_current;
       // if (counters.find( w_prev ) != counters.end())
//            accumulate(counters[w_prev],w_current);
    if (id_prev>=0)
    {
        accumulate(id_prev,id_current);
    //    std::cerr<<"inserting   "<<id_prev<<" , "<<id_current<<" ("<<w_current<<")\n";
    }
    //if (w_prev.length()!=0)
        //accumulate( get_id(tree,w_current.c_str()),get_id(tree,w_prev.c_str()    ) ) ;
//    
  //if (counters.find( w_current ) != counters.end())
//            accumulate(counters[w_current],std::string("-")+w_prev);
          //std::cout << w_prev<<" " << t << std::endl;
    id_prev=id_current;
    }
}

void load_bigrams(std::string str_path_in,const Options & options)
{
    DirReader dr(str_path_in);
    auto size_window = options.size_window;
    boost::circular_buffer<int64_t> cb(size_window); //- size of n-grams
    for (uint64_t i =0 ; i<size_window; i++) cb.push_back(-1);
    char * word;
    while ((word=dr.get_word())!=NULL )
    {
        if (vocab.is_word_valid(std::string(word)))
        {
            Index id_current = vocab.get_id(word);
            if (id_current>=0)
            {
                freq_per_id[id_current]++;
                cnt_words_processed++;
                cb.push_back(id_current);
                auto i = cb.begin();
                auto first = *i;
                for (size_t j=1;j<cb.size();j++)
                {
                   // std::cerr<<first<<"\t"<<cb[j]<<"\n";
                    accumulate(first,cb[j]);
                    accumulate(cb[j],first);
                }
            }
        }
    }
    //the rest of the list
    for (uint64_t i =0 ; i<size_window; i++) 
    {
        cb.push_back(-1);
        auto it = cb.begin();
        auto first = *it;
        for (size_t j=1;j<cb.size();j++)
        {
            accumulate(first,cb[j]);
            accumulate(cb[j],first);
        }
    }

}

struct window_params
{
    uint64_t size_window;
    bool symmetric;
};
int main(int argc, char * argv[])
{
    Options options = ProcessOptions(argc,argv);
    auto str_path_in = options.path_in.string();
    auto path_out=options.path_out;

    provenance = "source corpus : ";
    provenance = provenance + str_path_in + "\n";

    std::cerr<<"assigning ids\n";
    vocab.read_from_dir(str_path_in);

    provenance = provenance + "words in corpus : "+ FormatHelper::ConvertToStr(vocab.cnt_words_processed)+"\n";
    provenance = provenance + "unique words : "+ FormatHelper::ConvertToStr(vocab.cnt_words)+"\n";

    
    vocab.reduce(options.min_frequency);
    provenance=provenance+"minimal frequency: "+FormatHelper::ConvertToStr(options.min_frequency)+"\n";
    //provenance = provenance + "words in corpus : "+ FormatHelper::ConvertToStr(vocab.cnt_words_processed)+"\n";
    provenance = provenance + "unique words : "+ FormatHelper::ConvertToStr(vocab.cnt_words)+"\n";

    freq_per_id.resize(vocab.cnt_words);
    std::fill (freq_per_id.begin(),freq_per_id.end(),0);   
    std::cerr<<"dumping ids and frequencies\n";

    vocab.dump_ids((path_out / boost::filesystem::path("ids")).string());
    vocab.dump_frequency((path_out / boost::filesystem::path("frequencies")).string());

    write_value_to_file((path_out / boost::filesystem::path("cnt_unique_words")).string(),vocab.cnt_words);
    write_value_to_file((path_out / boost::filesystem::path("cnt_words")).string(),vocab.cnt_words_processed);

    std::cerr<<"extracting bigrams\n";

    //Index cnt_words_last_dump=0;
    //append_values_to_file((boost::filesystem::path(path_out) / boost::filesystem::path("cnt_bigrams")).string(),0,0,0);
    provenance+="windows size : "+FormatHelper::ConvertToStr(options.size_window);
    provenance+="\nfrequency weightening : PMI";
    load_bigrams(str_path_in,options);

    std::cerr<<"dumping results to disk\n";

    write_vector_to_file((path_out / boost::filesystem::path("freq_per_id")).string(),freq_per_id);
    dump_crs_bin(path_out.string());
    write_value_to_file((path_out / boost::filesystem::path("provenance.txt")).string(),provenance);
    //dump_crs(path_out.string());
 //   write_cooccurrence_text((path_out / boost::filesystem::path("bigrams_list")).string());

    return 0;
}