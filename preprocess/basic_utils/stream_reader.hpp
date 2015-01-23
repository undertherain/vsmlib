#include <boost/filesystem.hpp>

class DirReader
   {
    boost::filesystem::recursive_directory_iterator dir,initial;
    std::ifstream file_in;
    char buffer[MAX_STR_SIZE];
    size_t pos_line;
    std::string line_current;
public:
    DirReader(std::string _dir):dir(_dir,boost::filesystem::symlink_option::recurse),initial(_dir,boost::filesystem::symlink_option::recurse)
    {
        file_in.open(dir->path().string());
        std::cerr<<"processing \t"<<dir->path().string()<<" ... ";
        //reset();
    }
    void reset()
    {
        pos_line=0;
        dir=initial;
        if (file_in.is_open()) file_in.close();
        file_in.open(dir->path().string());
        std::cerr<<"processing \t"<<dir->path().string()<<" ... ";
    }

    bool check_simlink_and_advance()
    {
        if (is_symlink(dir->symlink_status())) 
        {
            file_in.close();
            dir++;
            std::cerr<<"we are in simlink - moving forward\nprocessing \t"<<dir->path().string()<<" ... ";
            file_in.open(dir->path().string());
            return true;
        }
        return false;
    }
    int check_eof_and_advance()
    {
        boost::filesystem::recursive_directory_iterator end;
        if (file_in.eof())
        {
            dir++;
            if (dir==end)
            {
                file_in.close();
                std::cerr<<"done \n";
                return -1;
            }
            else 
            {
                std::cerr<<"done \nprocessing \t"<<dir->path().string()<<" ... ";
                file_in.close();
                file_in.open(dir->path().string());
                return  0;
            }
       }
       return 1;
    }

    bool is_separator(char c)
    {
        for (size_t i=0;i<15;i++)
            if (c==separators[i]) return true;
        if (c==13) return true;
        if (c==10) return true;
        if (c<'a') return true;
        if (c>'z') return true;
        return false;
    }
    char * get_word()
    {
        size_t pos_buf=0;
        char ch;
        do 
        {
            if (check_simlink_and_advance()) continue;
            auto r= check_eof_and_advance();
            if (r<0) return NULL;
            if (r==0) continue;
            file_in.read(&ch,1);
            ch = tolower(ch);
            if (is_separator(ch)) 
            {
                if (pos_buf<2)
                {
                    pos_buf=0;
                    continue;
                }
                buffer[pos_buf]=0;
                return buffer;
            }
            buffer[pos_buf++]=ch;
        }   
        while(1);


        return buffer;
    }


    bool getline(std::string & line)
    {
        do
        {
            if (check_simlink_and_advance()) continue;
            auto r= check_eof_and_advance();
            if (r<0) return false;
            if (r==0) continue;
            std::getline(file_in, line);
            if (!is_line_valid(line)) continue;
            return true;
        }
        while(1);
    }
};