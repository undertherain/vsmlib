#include <set>

inline void trim3(std::string & str)
{
  str.erase(str.begin(), find_if(str.begin(), str.end(), [](char& ch)->bool { return !isspace(ch); }));
  str.erase(find_if(str.rbegin(), str.rend(), [](char& ch)->bool { return !isspace(ch); }).base(), str.end());
  for (unsigned int i=0;i<str.length();i++)
  {
  //	if (!isalpha(str[i])) str[i]='_';
  }
   //return str;
}  

inline void clean(std::string & str)
{
      trim3(str);
      std::transform(str.begin(), str.end(), str.begin(), ::tolower);
}

inline bool is_word_valid(std::string const & w)
{
	if (w.length()<3) return false;
	if (!std::isalpha(w[0])) return false;
	if (!std::isalpha(w[1])) return false;
	if(stopwords.find(w) != stopwords.end()) return false;
	return true;
}

bool hasEnding (std::string const &fullString, std::string const &ending)
{
    if (fullString.length() >= ending.length()) {
        return (0 == fullString.compare (fullString.length() - ending.length(), ending.length(), ending));
    } else {
        return false;
    }
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
