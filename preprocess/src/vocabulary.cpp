#include <iostream>
#include <string>  
#include <locale>
#include <boost/locale/encoding_utf.hpp>
#include <codecvt>
#include <set>
//#include <boost/tokenizer.hpp>
#include "basic_utils/stream_reader.hpp"
#include "basic_utils/utils.hpp"
//#include "ternary_tree.hpp"
#include "vocabulary.hpp"

template<class Facet>
struct deletable_facet : Facet
{
    template<class ...Args>
	deletable_facet(Args&& ...args) : Facet(std::forward<Args>(args)...) {}
	~deletable_facet() {}
};

Vocabulary::Vocabulary():cnt_words(0),cnt_words_processed(0){
	for (auto s : load_words("stopwords.txt"))
	{
		stopwords.insert(s);	
	}
}

inline bool Vocabulary::is_word_valid(std::string const & w)
{
	std::cerr<<"input: " <<w<<"\n";
		//std::wstring_convert<std::codecvt_utf8_utf32<wchar_t>,wchar_t> convert;
		//std::wstring ws = convert.from_bytes(w);   
	std::wstring_convert<deletable_facet<std::codecvt<char16_t, char, std::mbstate_t>>, char16_t> conv16;
	std::u16string str16 = conv16.from_bytes(w.c_str());
	static const std::locale loc("en_US.utf8");
		//size_t len= ws.length();
  		//std::wcout<<ws<<"\n";
		//std::cerr<<"length = "<<len<<"\n";
  		//if (len<3) return false;
  		//if (len>20) return false;
  		//std::cerr<<sizeof(ws[0])<<ws[0];

	if (!std::iswalpha(str16[0])) return false;
  		//if (!std::isalpha(w[1],loc)) return false;
  		//if (!std::isalpha(w[2],loc)) return false;
		//if(stopwords.find(w) != stopwords.end()) return false;
	//std::cerr<<"\t is good!\n";

	return true;
}

void Vocabulary::read_from_dir(std::string dir)
{
	DirReader dr(dir);
	char * word;
	while ((word=dr.get_word())!=NULL )
	{
		if (is_word_valid(std::string(word)))
		{
			tree.set_id_and_increment(word);	
			cnt_words_processed++;
		}
	}
	cnt_words=tree.id_global;
}
int64_t Vocabulary::get_id(const char * str)
{
	return tree.get_id(str);
}

void Vocabulary::reduce(int64_t threshold)
{
	size_t cnt_nodes=tree.count_nodes();
	std::cerr<<"3-tree node count = "<<cnt_nodes<<"\twill take "<<FormatHelper::SizeToHumanStr(cnt_nodes*sizeof(TernaryTreeNode<Index>))<<"\ntrimming the tree...\n";
	trim(&(tree.tree),threshold,0);
	cnt_nodes=tree.count_nodes();
	std::cerr<<"reduced node count = "<<cnt_nodes<<"\twill take "<<FormatHelper::SizeToHumanStr(cnt_nodes*sizeof(TernaryTreeNode<Index>))<<"\n";
	tree.reassign_ids();
	cnt_words=tree.id_global;
}

void Vocabulary::dump_frequency(const std::string & name_file) const
{
	tree.dump_frequency(name_file);
}

void Vocabulary::dump_ids(const std::string & name_file) const
{
	tree.dump_ids(name_file);	
}

void Vocabulary::populate_frequency(std::vector<Index> & lst_frequency )const
{
	tree.populate_frequency(lst_frequency);	
}

void Vocabulary::reassign_ids(std::vector<Index> const & lst_frequency)
{
	std::vector<Index> ids_new;
	for (size_t i=0;i<cnt_words;i++)
		ids_new.push_back(i);
	struct by_freq{ 
		std::vector<Index> const & lst_frequency;
		by_freq(std::vector<Index> const & _lst_frequency):lst_frequency(_lst_frequency){}
		bool operator()(Index a, Index b) 
		{ 
			return lst_frequency[a] > lst_frequency[b];
		}
	};
	std::sort(ids_new.begin(),ids_new.end(),by_freq(lst_frequency));
	std::vector<Index> ids_new2;
	ids_new2.resize(cnt_words);
	for (size_t i=0;i<cnt_words;i++)
	{
        //	std::cerr<<i<<"\t"<<ids_new[i]<<"\t"<<lst_frequency[ids_new[i]]<<"\n";
		ids_new2[ids_new[i]]=i;
	}
	tree.reassign_ids_new(ids_new2);
}
