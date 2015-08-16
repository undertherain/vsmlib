template<typename Type> 
void write_value_to_file(std::string name,Type value)
{
    std::ofstream file(name);
    file<<value;
    file.close();
}

template<typename Type> 
void write_values_to_file(std::ofstream &file,Type value)
{
    file<<value<<'\n';
}

template<typename T, typename ... Types> 
void write_values_to_file(std::ofstream &file,T head, Types ... tail)
{
    file<<head<<'\t';
    write_values_to_file(file,tail...);
}
template<typename ... Types> 
void write_values_to_file(std::string name, Types ... args)
{
    std::ofstream file(name);
//    std::cerr<<sizeof...(Types);//<<'\n';
    write_values_to_file(file,args...);
    file.close();
}
template<typename ... Types> 
void append_values_to_file(std::string name, Types ... args)
{
    std::ofstream file(name, std::ofstream::app);
//    std::cerr<<sizeof...(Types);//<<'\n';
    write_values_to_file(file,args...);
    file.close();
}

template <typename T>
void write_vector_to_file(std::string name,std::vector<T> const &  values)
{
    std::ofstream file(name);
    for (size_t i=0;i<values.size();i++)
//      file<<i<<"\t"<<values[i]<<"\n";
    {
        T v=values[i];
        file.write( reinterpret_cast<const char*>(&v),sizeof(T));
    }
     //   file<<values[i]<<"\n";
    file.close();
}

//double get_pmi()
//{
    //double v=log2((static_cast<double>(second.second)*cnt_words)/(freq_per_id[first.first]*freq_per_id[second.first]));
//}

void dump_crs(std::string path_out)
{
    std::ofstream file;
    std::string str_path = (boost::filesystem::path(path_out) / boost::filesystem::path("bigrams.data")).string();
    file.open (str_path);
    if(!file) throw  std::runtime_error("can not open output file "+str_path+" , check the path");
    for (size_t first=0;first<counters.size();first++)
        for (const auto& second : counters[first]) 
        {
            double v=log2((static_cast<double>(second.second)*vocab.cnt_words_processed)/(freq_per_id[first]*freq_per_id[second.first]));
            file<<v<<"\n";
        }
    file.close();
    str_path = (boost::filesystem::path(path_out) / boost::filesystem::path("bigrams.col_ind")).string();
    file.open (str_path);
    for (size_t first=0;first<counters.size();first++)
        for (const auto& second : counters[first]) 
        {
            file<<second.first<<"\n";
        }
    file.close();

    str_path = (boost::filesystem::path(path_out) / boost::filesystem::path("bigrams.row_ptr")).string();
    file.open (str_path);
    Index row_ptr=0;
    Index id_last=0;
    for (size_t first=0;first<counters.size();first++)
    {
        //std::cerr<<"first.first = "<<first.first<<"\t count = "<<first.second.size()<<"\n";
        if (first==0) file<<row_ptr<<"\n";
        else
            for (size_t k=id_last;k<first;k++)
                file<<row_ptr<<"\n";
            id_last=first;
            row_ptr+=counters[first].size();
        }
        for (size_t k=id_last;k<vocab.cnt_words;k++)
           file<<row_ptr<<"\n";

       file.close();
   }

void dump_crs_bin(std::string path_out)
{
    //std::ostringstream oss(std::ios::binary);
    std::ofstream file;
    std::string str_path = (boost::filesystem::path(path_out) / boost::filesystem::path("bigrams.data.bin")).string();
    file.open (str_path,  std::ios::out | std::ios::binary);
    //std::ios::binary 
    if(!file) throw  std::runtime_error("can not open output file "+str_path+" , check the path");
    for (size_t first=0;first<counters.size();first++)
        for (const auto& second : counters[first]) 
        {
            float v=log2((static_cast<double>(second.second)*vocab.cnt_words_processed)/(freq_per_id[first]*freq_per_id[second.first]));
            file.write( reinterpret_cast<const char*>(&v),sizeof(v));
        }
    
    file.close();
    str_path = (boost::filesystem::path(path_out) / boost::filesystem::path("bigrams.col_ind.bin")).string();
    file.open (str_path,  std::ios::out | std::ios::binary);
    for (size_t first=0;first<counters.size();first++)
        for (const auto& second : counters[first]) 
        {
            size_t v=second.first;
            file.write( reinterpret_cast<const char*>(&v),sizeof(v));
        }
    file.close();
    str_path = (boost::filesystem::path(path_out) / boost::filesystem::path("bigrams.row_ptr.bin")).string();
    file.open (str_path);
    size_t row_ptr=0;
    Index id_last=0;
    for (size_t first=0;first<counters.size();first++)
    {
        //std::cerr<<"first.first = "<<first<<"\t count = "<<first.second.size()<<"\n";
        if (first==0) file.write( reinterpret_cast<const char*>(&row_ptr),sizeof(row_ptr));
        else
            for (size_t k=id_last;k<first;k++)
                file.write( reinterpret_cast<const char*>(&row_ptr),sizeof(row_ptr));
            id_last=first;
            row_ptr+=counters[first].size();
        }
        for (size_t k=id_last;k<vocab.cnt_words;k++)
           file.write( reinterpret_cast<const char*>(&row_ptr),sizeof(row_ptr));

       file.close();
   }

void write_cooccurrence_text(std::string name_file)
{
std::ofstream file;
file.open (name_file);
if(!file) throw  std::runtime_error("can not open output file "+name_file+" , check the path");
for (size_t first=0;first<counters.size();first++)
{
    for (const auto& second : counters[first]) 
    {
      //if (t.second>0)
       // file<<first.first<<"\t"<<second.first<<"\t"<<second.second<<"\n";
        double v=log2((static_cast<double>(second.second)*vocab.cnt_words_processed)/(freq_per_id[first]*freq_per_id[second.first]));
        file<<first<<"\t"<<second.first<<"\t"<<v<<"\n";
    }
}

file.close();
}