#include <iostream>
#include <locale>
#include <codecvt>
#include "../basic_utils/stream_reader.hpp"



int main(int argc, char * argv[])
{
	std::cout<<"testing stream reader ... \n";

	std::string str_path_in(argv[1]);
	DirReader dr(str_path_in);
	wchar_t * word;
	std::cout<<"reading the word ... \n";
   	while ((word=dr.get_word())!=NULL )
   	{
   		std::wstring str(word);
   		std::cerr<<wstring_to_utf8(str)<<"\n";
    }
	std::cout<<"done!\n";

}