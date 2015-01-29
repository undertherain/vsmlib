#include <set>
#include <list>
#include <algorithm>
#include <fstream>

#define MAX_STR_SIZE  1500
const char separators[]=" .,:;!?()[]-\t\"'";


  
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



inline bool is_line_valid(std::string const & w)
{
  if (w.length()==0) return false;
  if ((w[0])=='<') return false;
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

std::list<std::string> load_words(std::string name_file)
{
  std::ifstream d_file(name_file);
    std::string line;
    std::list<std::string> result;
    while( std::getline( d_file, line ) ) 
    {
        trim3(line);
        result.push_back(line);
    }
    return result;
}