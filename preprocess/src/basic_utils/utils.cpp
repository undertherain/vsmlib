#include <ctime>
#include <list>
#include <iostream>
#include <stdio.h>
#include <stdlib.h>
#include "utils.hpp"


//--class buffer ---------------


void WriteToFile(byte  * buffer,unsigned long size,const char* name)
{
	FILE *file;
	//Open file
	file = fopen(name, "wb");
	if (!file)
	{
		fprintf(stderr, "Unable to open file %s", name);
		return;
	}
	fwrite(buffer, size, 1, file);
	fclose(file);
}

std::list<std::string> getFileList()
{
	std::string directory="./in";
	std::list<std::string> listFiles;
#if  defined(ARCH_WIN)
// Win32 API directory listing-------------
	std::string searchPattern="in/*.*";

	std::wstring wSearchPattern(searchPattern.length(), ' ');
	std::copy(searchPattern.begin(), searchPattern.end(), wSearchPattern.begin());

	HANDLE hFile;							 // Handle to file
	WIN32_FIND_DATA FileInformation;         // File information
	hFile = ::FindFirstFile(wSearchPattern.c_str(), &FileInformation);
	if(hFile != INVALID_HANDLE_VALUE)
	{
		do
		{
			if(FileInformation.cFileName[0] != '.')
			{
				if(FileInformation.dwFileAttributes & FILE_ATTRIBUTE_DIRECTORY)
				{
					//process subdirs
				}
				else
				{
					std::wstring  strFilePathW = (FileInformation.cFileName);
					///std::string strFilePath( strFilePathW.begin(), strFilePathW.end() );
					std::string strFilePath;
					FormatHelper::wstrToUtf8(strFilePath,strFilePathW);

					listFiles.push_back("in/"+strFilePath);
				}
			}
		} while(::FindNextFile(hFile, &FileInformation) == TRUE);
	}
	else
	{
		//logger.WriteLog("could not find files"); //todo proper error handling
	}
#else
 	//POSIX-specific directory listing---------------------------
	struct dirent **filelist;
	std::string temps;
	int n;
	n=scandir(directory.c_str(),&filelist,0,alphasort);
	if (n<0)
	{
		std::cerr<<"no file found"<<std::endl;
		//should we exit here?
	} else
	{
		for (int ii=0;ii<n;ii++)
		{
			temps=filelist[ii]->d_name;
			free (filelist[ii]);
			if  (temps.find("*")!=std::string::npos)
			{
				std::cout<<"loading   "<<temps<<std::endl;
				//decks.push_back(DeckInfo(temps));//todo
			}
		}
		free(filelist);
	//	std::cout<<n<<" decks file"<<std::endl;
	}
#endif
	return listFiles;
}


