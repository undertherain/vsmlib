#include <iostream>
#include <list>
#include <locale>
#include <codecvt>

#include "../vocabulary.hpp"


int main()
{
	std::cout<<"testing vocabulary\n";
	Vocabulary vocab;
    vocab.read_from_dir("dirtest/test_repeat");

    std::cerr << "words in corpus : " << vocab.cnt_words_processed << "\n";
    std::cerr << "unique words : " << vocab.cnt_words << "\n";

    vocab.dump_ids("vocab.ids");
    vocab.dump_frequency("vocab.frequencies");
    
	return 0;
}