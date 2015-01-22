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

typedef int64_t Index;
const char separators[]=" .,:;!?()[]-\t\"'";

#include "string_tools.hpp"
#include "ternary_tree.hpp"
#include "basic_utils/utils.hpp"
#include "basic_utils/stream_reader.hpp"
#include "vocabulary.hpp"

//Index cnt_words;
//Index cnt_unique_words;
Index cnt_words_processed;
Index cnt_bigrams;
Index current_max;
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
 std::string w_prev;
for (const auto& t : tokens) {
    std::string w_current=t;
    clean(w_current);
    if (!vocab.is_word_valid(w_current))  continue;
    Index id_current=vocab.get_id(w_current.c_str());
    if (id_current<0) continue;
    freq_per_id[id_current]++;
    cnt_words_processed++;
    if (current_max<id_current) current_max=id_current;
       // if (counters.find( w_prev ) != counters.end())
//            accumulate(counters[w_prev],w_current);
    if (w_prev.length()>1)
    {
            //if get_id(tree,w_prev.c_str())
        accumulate(vocab.get_id(w_prev.c_str()),id_current);
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

int main(int argc, char * argv[])
{
 if (argc<3)
 {
  std::cerr << "usage: " << argv[0] << " corpus_dir output_dir \n";
  return 0;
}
std::string str_path_in (argv[1]);
boost::filesystem::path path_out(argv[2]);
///write_values_to_file((path_out / boost::filesystem::path("cnt_bigrams")).string(),"cnt_words","cnt_unique_words","cnt_bigrams");

std::cerr<<"assigning ids\n";
vocab.read_from_dir(str_path_in);
//cnt_unique_words=vocab.cnt_words;
vocab.reduce();

freq_per_id.resize(vocab.cnt_words);

std::cerr<<"dumping ids and frequencies\n";

vocab.dump_ids((path_out / boost::filesystem::path("ids")).string());
vocab.dump_frequency((path_out / boost::filesystem::path("frequencies")).string());

write_value_to_file((path_out / boost::filesystem::path("cnt_unique_words")).string(),vocab.cnt_words);
write_value_to_file((path_out / boost::filesystem::path("cnt_words")).string(),vocab.cnt_words_processed);
//return 0;

std::cerr<<"extracting bigrams\n";
DirReader dr(str_path_in);
///dr.reset();
Index cnt_words_last_dump=0;
        append_values_to_file((boost::filesystem::path(path_out) / boost::filesystem::path("cnt_bigrams")).string(),0,0,0);
std::string line;
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

write_vector_to_file((path_out / boost::filesystem::path("freq_per_id")).string(),freq_per_id);
dump_crs_bin(path_out.string());
//write_cooccurrence_text((path_out / boost::filesystem::path("bigrams_list")).string());

//dump_crs(path_out.string());
return 0;
}