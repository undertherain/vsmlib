#include <boost/program_options.hpp>
namespace program_options = boost::program_options;

struct Options
{
    std::vector<std::string> namesFilesQry;
    std::string mode;
    uint64_t size_window;
    uint64_t min_frequency;
    boost::filesystem::path path_in;
    //std::string path_out;
    boost::filesystem::path path_out;
    bool verbose;
    Options():verbose(false)
    {}
};

Options ProcessOptions(const int argc, char * const argv[])
{
    program_options::options_description optionsDescription("options");
    Options options;
    program_options::positional_options_description pos;
    pos.add("source_dir", 1);
    pos.add("destination_dir", 2);

    optionsDescription.add_options()
        ("help,h", "produce help message")
        ("source_dir", program_options::value<boost::filesystem::path>(&options.path_in)->required(), "source dir")
        ("destination_dir", program_options::value< boost::filesystem::path > (&options.path_out)->required(), "destination dir")
        ("window_size", program_options::value<uint64_t>(&(options.size_window))->default_value(2), "window size")
        ("minimal_frequency", program_options::value<uint64_t>(&(options.min_frequency))->default_value(10), "mimimal word frequency")
        //("mode", program_options::value<std::string>(&(options.mode))->default_value("multi"), "execution mode")
        ;
    program_options::variables_map optionsMap;

    try
    {
        program_options::store(program_options::command_line_parser(argc, argv).options(optionsDescription).positional(pos).run(), optionsMap);
        program_options::notify(optionsMap);
    }
    catch (const std::exception& e)
    {
        std::cerr << "command line error: " << e.what() << std::endl;
        std::cout << optionsDescription << std::endl;
        exit(-1);
    }

    if (optionsMap.count("help"))
    {
        std::cout << "Usage: "<<argv[0]<<" [options] <source dir> <destination dir> \n";
        std::cout << optionsDescription << std::endl;
        exit(0);
    }

    if (optionsMap.count("reference-file"))
    {

    }
//  {
//      std::cout << "reference file: ";
//      std::cout << options.nameFileRef << "\n";
//      std::cout << options.namesFilesQry[1]<<std::endl;
//  }

    return options;
}
