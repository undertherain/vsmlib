#include <iostream>
#include <string>  
#include <locale>
#include <boost/locale/encoding_utf.hpp>
//#include <codecvt>
#include <set>
//#include <boost/tokenizer.hpp>
#include "basic_utils/stream_reader.hpp"
#include "basic_utils/utils.hpp"
#include "vocabulary.hpp"


Vocabulary::Vocabulary():cnt_words(0),cnt_words_processed(0),locale(std::locale("en_US.UTF8")){
	for (auto s : load_words("stopwords.txt"))
	{
		stopwords.insert(s);	
	}
}

bool Vocabulary::is_word_valid(std::wstring const & w)
{
	//std::cerr<<"input: " <<wstring_to_utf8(w)<<"\n";
	size_t len= w.length();
	if (len<1) return false;
  	if (len>20) return false;
	//if (!std::isalpha(w[0],locale)) return false;
  	//if (!std::isalpha(w[1],locale)) return false;
	//if(stopwords.find(w) != stopwords.end()) return false;
	//std::cerr<<"\t is good!\n";
	return true;
}

void Vocabulary::read_from_dir(std::string dir)
{
	DirReader dr(dir);
	wchar_t * word;
	while ((word=dr.get_word())!=NULL )
	{
		if (is_word_valid(std::wstring(word)))
		{
			tree.set_id_and_increment(word);	
			cnt_words_processed++;
		}
	}
	cnt_words=tree.id_global;
}
int64_t Vocabulary::get_id(const wchar_t * str)
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
