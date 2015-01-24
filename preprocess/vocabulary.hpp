#include <iostream>
#include <set>
#include <boost/tokenizer.hpp>
//#include "string_tools.hpp"
#include "basic_utils/stream_reader.hpp"
#include "basic_utils/utils.hpp"
#include "ternary_tree.hpp"



class Vocabulary
{
	std::set<std::string> stopwords;
	TernaryTree tree;
	void process_sentence_ids(std::string const & s)
	{
	    /*if (s.length()<2) return;
	    boost::char_separator<char> sep(separators);
	    boost::tokenizer<boost::char_separator<char> > tokens(s, sep);
	    for (const auto& t : tokens) {
        	std::string str = t;
        	clean(str);
        	if (!is_word_valid(str)) continue;
        	cnt_words_processed++;
        	tree.set_id_and_increment(str.c_str());
    	}
    	*/
	}	
public:
	size_t cnt_words;
	size_t cnt_words_processed;
	Vocabulary():cnt_words(0),cnt_words_processed(0){
		for (auto s : load_words("stopwords.txt"))
		{
			stopwords.insert(s);	
		}
	}
	inline bool is_word_valid(std::string const & w)
	{
		size_t len= w.length();
  		if (len<3) return false;
  		if (len>20) return false;
		if (!std::isalpha(w[0])) return false;
  		if (!std::isalpha(w[1])) return false;
  		if (!std::isalpha(w[2])) return false;
		if(stopwords.find(w) != stopwords.end()) return false;
	return true;
	}
	void read_from_dir(std::string dir)
	{
		DirReader dr(dir);
		//std::string line;
		//while (dr.getline(line) )
		//{
		    //process_sentence_ids(line);
		//}
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
	int64_t get_id(const char * str)
	{
		return tree.get_id(str);
	}
	void reduce()
	{
		size_t cnt_nodes=tree.count_nodes();
		std::cerr<<"3-tree node count = "<<cnt_nodes<<"\twill take "<<FormatHelper::SizeToHumanStr(cnt_nodes*sizeof(TernaryTreeNode<Index>))<<"\ntrimming the tree...\n";
		trim(&(tree.tree),0);
		cnt_nodes=tree.count_nodes();
		std::cerr<<"reduced node count = "<<cnt_nodes<<"\twill take "<<FormatHelper::SizeToHumanStr(cnt_nodes*sizeof(TernaryTreeNode<Index>))<<"\n";
		tree.reassign_ids();
		cnt_words=tree.id_global;
	}
    void dump_frequency(const std::string & name_file) const
    {
    	tree.dump_frequency(name_file);
    }
    void dump_ids(const std::string & name_file) const
    {
    	tree.dump_ids(name_file);	
    }


};
