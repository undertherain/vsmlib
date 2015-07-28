#include <list>
//#include <fstream>

#if !defined(MAX_STR_SIZE)
#define MAX_STR_SIZE  1500
#endif

const char separators[]=" .,:;!?()[]-\t\"'";
  
inline void trim3(std::string & str);
inline void clean(std::string & str);
bool is_line_valid(std::string const & w);
bool hasEnding (std::string const &fullString, std::string const &ending);
std::list<std::string> load_words(std::string name_file);
