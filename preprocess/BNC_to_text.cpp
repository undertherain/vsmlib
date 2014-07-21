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
std::set<std::string> stopwords;


bool hasEnding (std::string const &fullString, std::string const &ending)
{
    if (fullString.length() >= ending.length()) {
        return (0 == fullString.compare (fullString.length() - ending.length(), ending.length(), ending));
    } else {
        return false;
    }
}

void trim3(std::string & str)
{
  str.erase(str.begin(), find_if(str.begin(), str.end(), [](char& ch)->bool { return !isspace(ch); }));
  str.erase(find_if(str.rbegin(), str.rend(), [](char& ch)->bool { return !isspace(ch); }).base(), str.end());
  //return str;
}  

void load_stopwords()
{
  std::ifstream d_file("stopwords.txt");
    std::string line;
    while(std::getline( d_file, line ) ) 
    {
        trim3(line);
        stopwords.insert( line );
    }
}

inline bool is_word_valid(std::string const & w)
{
	if (w.length()<3) return false;
  if (!std::isalpha(w[0])) return false;
	if(stopwords.find(w) != stopwords.end()) return false;
	return true;
}

void traverse(const ptree & pt)
{
    for(ptree::const_iterator iter = pt.begin(); iter != pt.end(); iter++)
	{
		if (iter->first=="w") 
		{
			cnt_words++;
			std::string w=iter->second.data();
			trim3(w);
      std::transform(w.begin(), w.end(), w.begin(), ::tolower);
			if (is_word_valid(w))
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
	load_stopwords();
  myfile.open (argv[2]);
// 	process_file_boost("/mnt/storage/Corpora/BNC/H/HY/HYG.xml");
	recursive_process_dir(argv[1]);
	myfile.close();
	std::cerr<<cnt_words<<" words processed\n";
	return 0;
}
