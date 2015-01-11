void write_value_to_file(std::string name,Index value)
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

void write_vector_to_file(std::string name,std::vector<Index> const &  values)
{
    std::ofstream file(name);
    for (Index i=0;i<values.size();i++)
        file<<i<<"\t"<<values[i]<<"\n";
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
    for (const auto& first : counters)  //vriting data
    {
        for (const auto& second : first.second) 
        {
            double v=log2((static_cast<double>(second.second)*cnt_words)/(freq_per_id[first.first]*freq_per_id[second.first]));
            file<<v<<"\n";
        }
    }
    file.close();
    str_path = (boost::filesystem::path(path_out) / boost::filesystem::path("bigrams.col_ind")).string();
    file.open (str_path);
    for (const auto& first : counters)  //vriting columnt indices
    {
        for (const auto& second : first.second) 
        {
            file<<second.first<<"\n";
        }
    }
    file.close();
    str_path = (boost::filesystem::path(path_out) / boost::filesystem::path("bigrams.row_ptr")).string();
    file.open (str_path);
    Index row_ptr=0;
    Index id_last=0;
    for (const auto& first : counters)  //vriting columnt indices
    {
        //std::cerr<<"first.first = "<<first.first<<"\t count = "<<first.second.size()<<"\n";
        if (first.first==0) file<<row_ptr<<"\n";
        else
            for (Index k=id_last;k<first.first;k++)
                file<<row_ptr<<"\n";
            id_last=first.first;
            row_ptr+=first.second.size();
        }
        for (Index k=id_last;k<id_global;k++)
           file<<row_ptr<<"\n";

       file.close();
   }
