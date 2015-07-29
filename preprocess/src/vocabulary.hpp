#include <iostream>
#include <string>  
#include <locale>
#include <boost/locale/encoding_utf.hpp>
//#include <codecvt>
#include <set>
//#include <boost/tokenizer.hpp>
//#include "basic_utils/stream_reader.hpp"
//#include "basic_utils/utils.hpp"
#include "ternary_tree.hpp"

class Vocabulary
{
	std::set<std::wstring> stopwords;
	TernaryTree tree;
public:
    size_t cnt_words;
    size_t cnt_words_processed;
    const std::locale locale;
    Vocabulary();
    bool is_word_valid(std::wstring const & w);
    void read_from_dir(std::string dir);
    void dump_frequency(const std::string & name_file) const;
    void dump_ids(const std::string & name_file) const;
    void populate_frequency(std::vector<Index> & lst_frequency )const;
    void reassign_ids(std::vector<Index> const & lst_frequency);
	int64_t get_id(const wchar_t * str);
	void reduce(int64_t threshold=5);
};
