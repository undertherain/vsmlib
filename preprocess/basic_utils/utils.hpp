
#ifndef MINDCRAFT_UTILS
#define MINDCRAFT_UTILS


//#include "exceptions.hpp"
//#include "buffer.hpp"

#include <exception>
#include <stdexcept>
#include <sstream>
#include <list>
#include <cmath>

#if  defined(ARCH_WIN)
    #include <windows.h>
#else
	#include <dirent.h>
#endif

#include "types.hpp"

void WriteToFile(byte  * buffer,unsigned long size,const char* name);

class FormatHelper
{
public:
#if  defined(ARCH_WIN)
	static void wstrToUtf8(std::string& dest, const std::wstring& src)
	{
		dest.clear();
		for (size_t i = 0; i < src.size(); i++){
			wchar_t w = src[i];
			if (w <= 0x7f)
				dest.push_back((char)w);
			else if (w <= 0x7ff){
				dest.push_back(0xc0 | ((w >> 6)& 0x1f));
				dest.push_back(0x80| (w & 0x3f));
			}
			else if (w <= 0xffff){
				dest.push_back(0xe0 | ((w >> 12)& 0x0f));
				dest.push_back(0x80| ((w >> 6) & 0x3f));
				dest.push_back(0x80| (w & 0x3f));
			}
			else if (w <= 0x10ffff){
				dest.push_back(0xf0 | ((w >> 18)& 0x07));
				dest.push_back(0x80| ((w >> 12) & 0x3f));
				dest.push_back(0x80| ((w >> 6) & 0x3f));
				dest.push_back(0x80| (w & 0x3f));
			}
			else
				dest.push_back('?');
		}
	}
#endif


	template <typename T>
	static std::string ConvertToStr(const T & val)
	{
		std::ostringstream out;
		out << val;
		std::string str = out.str();
		return str;
	}
	static int StrToInt(const std::string & str)
	{
		int value;
		std::istringstream tempStream(str);
		tempStream>>value;
		return value;
	}
	static float StrToFloat(const std::string & str)
	{
		float value;
		std::istringstream tempStream(str);
		tempStream>>value;
		return value;
	}
	static std::string SizeToHumanStr(double size)
	{
	    std::string suffixes[]={"B","KB","MB","GB","TB","PB"};

        std::string fract="";
        for (int i=0;i<5;i++)
        {

            if (size<1024)
            return ConvertToStr(size)+suffixes[i];
            //fract="."+ConvertToStr(size % 1024).substr(0,1);
            size=floor(size/102.4)/10;
        }

        return "so huge!!!";
	}
};

std::list<std::string> getFileList();

#endif //MINDCRAFT_UTILS
