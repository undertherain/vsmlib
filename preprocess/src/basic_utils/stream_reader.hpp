#include <boost/filesystem.hpp>
#include <fstream>
#include "../string_tools.hpp"

class DirReader
   {
    boost::filesystem::recursive_directory_iterator dir,initial;
    std::ifstream file_in;
    char buffer[MAX_STR_SIZE];
    std::string line_current;
public:
    DirReader(std::string _dir);
    void reset();
    bool check_simlink_and_advance();
    int check_eof_and_advance();
    bool is_separator(char c);
    char * get_word();
    bool getline(std::string & line);
};