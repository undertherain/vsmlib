#include <iostream>
#include <boost/filesystem.hpp>
#include "stream_reader.hpp"

DirReader::DirReader(std::string _dir):dir(_dir,boost::filesystem::symlink_option::recurse),initial(_dir,boost::filesystem::symlink_option::recurse),locale(std::locale("en_US.UTF8"))
{
        //file_in.open(dir->path().string());
        //std::cerr<<"processing \t"<<dir->path().string()<<" ... \n";
    reset();
}
void DirReader::reset()
{
       // pos_line=0;
    dir=initial;
    boost::filesystem::recursive_directory_iterator end;
    while (!(boost::filesystem::is_regular_file(dir->status())))
    {
        dir++;
        if (dir==end)
            return;
    }   

    if (file_in.is_open()) file_in.close();
    file_in.open(dir->path().string());
    file_in.imbue(locale);
    std::cerr<<"processing \t"<<dir->path().string()<<" ... \n";
}

bool DirReader::check_simlink_and_advance()
{
    if (is_symlink(dir->symlink_status())) 
    {
        file_in.close();
        dir++;
        std::cerr<<"we are in simlink - moving forward\nprocessing \t"<<dir->path().string()<<" ... \n";
        file_in.open(dir->path().string());
        return true;
    }
    return false;
}
int DirReader::check_eof_and_advance()
{
    boost::filesystem::recursive_directory_iterator end;
    if (file_in.eof())
    {
        dir++;
        if (dir==end)
        {
            file_in.close();
            std::cerr<<"all done! \n";
            return -1;
        }
        else 
        {
            std::cerr<<"processing \t"<<dir->path().string()<<" ... \n";
            file_in.close();
            file_in.open(dir->path().string());
            return  0;
        }
    }
    return 1;
}

bool DirReader::is_separator(wchar_t c)
{
    for (size_t i=0;i<15;i++)
        if (c==separators[i]) return true;
    if (c==13) return true;
    if (c==10) return true;
       // if (c<'a') return true;
       // if (c>'z') return true;
    return false;
}
wchar_t * DirReader::get_word_raw()
{
    if (!myqueue.empty())
    {
        wcscpy(buffer,myqueue.front().c_str());
        myqueue.pop();
        return buffer;
    }
    boost::filesystem::recursive_directory_iterator end;
    size_t pos_buf=0;
    wchar_t ch;
    do 
    {
        //std::cerr<<"we are in dat loop \n";
        if (file_in.eof()) 
        {
            if (pos_buf>1) 
            {
                buffer[pos_buf=0];
                return buffer;
            }
            do
            {
                dir++;
                if (dir==end)
                    return NULL;
            }   while (!(boost::filesystem::is_regular_file(dir->status())));
            file_in.close();
            std::cerr<<"processing \t"<<dir->path().string()<<" ... \n";
            file_in.open(dir->path().string());
            file_in.imbue(locale);
            pos_buf=0;
        }
        file_in.read(&ch,1);
        if (file_in.eof()) 
            {
                //std::cerr<<"we are EOF\n";
                continue;
            }
        //std::cerr<<"just read "<<ch<<"\n";
        ch = tolower(ch,locale);
        if (is_separator(ch)) 
        {
            //std::cerr<<"this is separator\n";
            buffer[pos_buf]=0;
            if (pos_buf<1)
            {
                pos_buf=0;
                continue;
            }
            if (ch==L'.')
            {
                myqueue.push(std::wstring(L"."));
            }
            return buffer;
        }
        buffer[pos_buf++]=ch;

    }   
    while(1);


    return NULL;
}

wchar_t * DirReader::get_word()
{
    wchar_t * ptr = clean_ptr(get_word_raw());
    return ptr;
}
/*
bool DirReader::getline(std::string & line)
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
*/