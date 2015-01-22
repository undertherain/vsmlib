class DirReader
   {
    boost::filesystem::recursive_directory_iterator dir,initial;
    std::ifstream file_in;
public:
    DirReader(std::string _dir):dir(_dir,boost::filesystem::symlink_option::recurse),initial(_dir,boost::filesystem::symlink_option::recurse)
    {
        file_in.open(dir->path().string());
        std::cerr<<"processing \t"<<dir->path().string()<<" ... ";
        //reset();
    }
    void reset()
    {
        dir=initial;
        if (file_in.is_open()) file_in.close();
        file_in.open(dir->path().string());
        std::cerr<<"processing \t"<<dir->path().string()<<" ... ";
    }
    bool getline(std::string & line)
    {
        boost::filesystem::recursive_directory_iterator end;
        do
        {
        if (is_symlink(dir->symlink_status())) 
        {
            file_in.close();
            dir++;
            std::cerr<<"we are in simlink - moving forward\nprocessing \t"<<dir->path().string()<<" ... ";
            file_in.open(dir->path().string());
            continue;
        }
        if (!file_in.eof())
        {
            std::getline(file_in, line);
            //std::cerr<<line<<"\n";
            if (!is_line_valid(line)) continue;
            //std::cerr<<line<<"is valid!\n";
            return true;
        } else 
        {
            dir++;
            if (dir==end)
            {
                file_in.close();
                std::cerr<<"done \n";
                return false;
            }
            else 
            {
                std::cerr<<"done \nprocessing \t"<<dir->path().string()<<" ... ";
                file_in.close();
                file_in.open(dir->path().string());
                if (!file_in.is_open()) {continue; }
                //std::getline(file_in, line);
                //return true;
            }
        }
        }
        while(1);
    }
};