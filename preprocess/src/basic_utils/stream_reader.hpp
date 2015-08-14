#include <boost/filesystem.hpp>
#include <fstream>
#include <queue>
#include "../string_tools.hpp"

class DirReader
   {
    boost::filesystem::recursive_directory_iterator dir,initial;
    std::wifstream file_in;
    wchar_t buffer[MAX_STR_SIZE];
    std::string line_current;
    const std::locale locale;
public:
    DirReader(std::string _dir);
    void reset();
    bool check_simlink_and_advance();
    int check_eof_and_advance();
    bool is_separator(wchar_t c);
    wchar_t * get_word_raw();
    wchar_t * get_word();
    std::queue<std::wstring> myqueue;
    //bool getline(std::string & line);
};