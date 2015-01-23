#include <iostream>
#include <cstring>
#include <fstream>
#include <set>
#include <algorithm>
#include <boost/filesystem.hpp>
#include <boost/property_tree/xml_parser.hpp>
#include <boost/property_tree/ptree.hpp>

std::ofstream myfile;

using boost::property_tree::ptree;

unsigned long long cnt_words;

//#include "string_tools.hpp"
#include "vocabulary.hpp"
Vocabulary vocab;



void traverse(const ptree & pt)
{
    for(ptree::const_iterator iter = pt.begin(); iter != pt.end(); iter++)
	{
		if (iter->first=="w") //hw
		{
			cnt_words++;
			std::string w=iter->second.data();
			clean(w);
			if (vocab.is_word_valid(w))
			myfile << w <<" ";
		}
		traverse(iter->second);
		if (iter->first=="s") 
			myfile << "\n";
		if (iter->first=="p") 
			myfile << "\n";
	}
}

void process_file_boost(std::string filename)
{
    std::ifstream is;
    is.open(filename); 
    ptree pt;
    read_xml(is, pt);
 	  traverse(pt);
}

void recursive_process_dir(std::string directory)
{
   for ( boost::filesystem::recursive_directory_iterator end, dir(directory);
    dir != end; ++dir ) {
    // std::cout << *dir << "\n";  // full path
    std::string path = dir->path().string();
    if (hasEnding( path,std::string(".xml")))
    {
    	std::cout << "processing" <<path << "\n"; // just last bit
    	process_file_boost(path);
    }
  }
}

int main(int argc, char * argv[])
{
  if (argc<3)
  {
      std::cerr << "usage: " << argv[0] << " path_to_BNC output_file\n";
      return 0;
  }
	//load_stopwords();
  myfile.open (argv[2]);
// 	process_file_boost("/mnt/storage/Corpora/BNC/H/HY/HYG.xml");
	recursive_process_dir(argv[1]);
	myfile.close();
	std::cerr<<cnt_words<<" words processed\n";
	return 0;
}
