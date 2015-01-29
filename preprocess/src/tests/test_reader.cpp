#include "../basic_utils/stream_reader.hpp"

int main(int argc, char * argv[])
{
	std::cout<<"testing stram reader\n";

	std::string str_path_in(argv[1]);
	DirReader dr(str_path_in);
	char * word;
   	while ((word=dr.get_word())!=NULL )
   	{
   		std::cerr<<word<<"\n";
    }
	std::cout<<"done!\n";

}