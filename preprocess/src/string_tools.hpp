#pragma once
#include <list>
//#include <fstream>

#if !defined(MAX_STR_SIZE)
#define MAX_STR_SIZE  15000
#endif

const char separators[]=" .,:;!?()[]-\t\"'";
  
std::string wstring_to_utf8 (const std::wstring& str);
inline void trim3(std::wstring & str);
inline void clean(std::string & str);
wchar_t * clean_ptr(wchar_t * str);
bool is_line_valid(std::string const & w);
bool hasEnding (std::string const &fullString, std::string const &ending);
std::list<std::wstring> load_words(std::string name_file);
