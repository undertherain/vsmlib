#include <fstream>
#include <algorithm>
#include <locale>
#include <codecvt>
#include "string_tools.hpp"
#include <iostream>
//#if !defined(MAX_STR_SIZE)
//#define MAX_STR_SIZE  1500
//#endif
//const char separators[]=" .,:;!?()[]-\t\"'";

  
std::string wstring_to_utf8 (const std::wstring& str)
{
    std::wstring_convert<std::codecvt_utf8<wchar_t>> myconv;
    return myconv.to_bytes(str);
}

inline void trim3(std::wstring & str)
{
  //str.erase(str.begin(), find_if(str.begin(), str.end(), [](char& ch)->bool { return !isspace(ch); }));
  //str.erase(find_if(str.rbegin(), str.rend(), [](char& ch)->bool { return !isspace(ch); }).base(), str.end());
  //for (unsigned int i=0;i<str.length();i++)
  //{
  //	if (!isalpha(str[i])) str[i]='_';
  //}
   //return str;
}  

inline void clean(std::wstring & str)
{
      trim3(str);
      std::transform(str.begin(), str.end(), str.begin(), ::tolower);
}

wchar_t * clean_ptr(wchar_t * str)
{
  if (str==NULL) return NULL;
  static const std::locale locale("en_US.UTF8");
  unsigned int length = wcslen(str);
  if ((length==1) && (*str==L'.')) return str;
  wchar_t * new_ptr = str;
  while ((!std::isalpha(new_ptr[0],locale)) && (new_ptr<str+length)) new_ptr++;
  wchar_t * end_ptr=str+length;
//  if ( (new_ptr[0]==L'б') && (new_ptr[1]==L'е') && (new_ptr[2]==L'ж') && (new_ptr[3]==L'а') && (new_ptr[4]==L'т'))
//  {
//  std::cerr<<wstring_to_utf8(new_ptr)<<" "<<wcslen(new_ptr)<<" "<<new_ptr[6]<<"\n";
  //std::cerr<<"endptr = "<<end_ptr<<"\n";
  while (((!std::isalpha(*end_ptr,locale)) || (*end_ptr==160))&& (end_ptr>new_ptr)) end_ptr--;
  *(end_ptr+1)=0;
//  }
  return new_ptr;
}


bool is_line_valid(std::string const & w)
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

std::list<std::wstring> load_words(std::string name_file)
{
  std::wifstream d_file(name_file);
  d_file.imbue(std::locale("en_US.UTF8"));
  std::wstring line;
  std::list<std::wstring> result;
  while( std::getline( d_file, line ) ) 
    {
        trim3(line);
        result.push_back(line);
    }
    return result;
}