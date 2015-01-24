#include <string>
#include <stdexcept>
#include <cstdio>
#include <cstring>
#include <vector>
#include <list>

#include "buffer_byte.hpp"
//#include "basic_utils/utils.hpp"
//#include "basic_utils/exceptions.hpp"

void BufferByte::Init()
{
    offsetChunk=0;
}

BufferByte::BufferByte()
{
    Init();
}

/*
Buffer::Buffer(std::string str)
{
    Init();
    size=str.length();
    buffer=new byte[size+1];
    for (Index i=0; i<size; i++)
        buffer[i]=CodeSymbol(str[i]);
    buffer[size]=0;
}
*/

BufferByte::~BufferByte()
{
#ifdef PRINT_ALL
    std::cout<<"destructing bytebuffer";
#endif
}

bool BufferByte::less(Index r,Index l)
{
    return std::strcmp(reinterpret_cast<const char *>(buffer+l), reinterpret_cast<const char *>(buffer+r)) < 0;
}

byte & BufferByte::operator[](const Index idx) const
{
    if (idx>size)
    {
        std::cerr<<"buffer [] index overflow"<<std::endl;
        throw std::exception();
    }//todo remove to debug
    return buffer[idx];
};

//global utils---------------------
Index LoadBytesFromFile(byte ** buffer,std::string nameFileIn)
{
    size_t sizeBuf;
    FILE *fileIn;
    fileIn=fopen(nameFileIn.c_str(), "rb");
    if (!fileIn)
    {
        throw std::runtime_error(std::string("file error in Buffer::loadFromFile: can not open ")+nameFileIn);    //todo!!!
    }
    //Get file length
    fseek(fileIn, 0, SEEK_END);
    sizeBuf=ftell(fileIn);
    fseek(fileIn, 0, SEEK_SET);

    *buffer=new byte[sizeBuf+1];  //todo - sheck if nit null
    if (!*buffer)
    {
        throw std::runtime_error("memory error in bufferbyte::loadFromFile");  
    }
    size_t cnt_read = fread(*buffer, 1, sizeBuf, fileIn);
    if (cnt_read<sizeBuf) std::cerr<<"read less ("<<cnt_read<<") than file size ("<<sizeBuf<<")\n";
    fclose(fileIn);
    return sizeBuf;
}

BufferByte BufferByte::LoadFromFile(std::string nameFileIn)
{
    BufferByte newBuffer;
    newBuffer.size=LoadBytesFromFile(&(newBuffer.buffer),nameFileIn);
    return newBuffer;
}


void BufferByte::Print() const
{
    for (Index i=0; i<20; i++)
    {
        std::cout<<buffer[i];
    }
    std::cout<<std::endl;
}
/*
BufferByte BufferByte::LoadFromDir()
{
    byte* _buffer;
    unsigned long sizeBuf;

    std::list<std::string> listFiles=getFileList();
    sizeBuf=0;
    for(std::list<std::string>::iterator iterFileName = listFiles.begin(); iterFileName != listFiles.end(); iterFileName++)
    {
        std::cout<<"getting size "<<*iterFileName<<std::endl;
        //char * inFileName="in.txt";
        FILE *fileIn;
        //Open file
        fileIn = fopen(iterFileName->c_str(), "rb");
        if (!fileIn)
        {
            fprintf(stderr, "Unable to open file %s", iterFileName->c_str());
            throw Exception("file error in Corpora::loadFromFile");    //todo!!!
        }
        //Get file length
        fseek(fileIn, 0, SEEK_END);
        sizeBuf+=ftell(fileIn);
        fclose(fileIn);
    }
    //now loading into one buffer

    //Allocate memory
    _buffer=new byte[sizeBuf+1];
    if (!_buffer)
    {
        fprintf(stderr, "Memory error!");
        throw std::exception();   //todo
    }
    unsigned char* posWriteBuffer=_buffer;
    for(std::list<std::string>::iterator iterFileName = listFiles.begin(); iterFileName != listFiles.end(); iterFileName++)
    {
        std::cout<<"loading "<<*iterFileName<<std::endl;
        FILE *fileIn;

        //Open file
        fileIn=fopen(iterFileName->c_str(), "rb");
        if (!fileIn)
        {
            fprintf(stderr, "Unable to open file %s", iterFileName->c_str());
            throw std::exception();
        }

        //Read file contents into buffer
        fseek(fileIn, 0, SEEK_END);
        int sizeCurrent=ftell(fileIn);
        //printf("File length=%d\n",sizeCurrent);
        fseek(fileIn, 0, SEEK_SET);

        fread(posWriteBuffer, sizeCurrent, 1, fileIn);
        posWriteBuffer+=sizeCurrent;
        fclose(fileIn);
    }
    printf("Corpora size=%lu\n",sizeBuf);
    Buffer newBuffer;
    newBuffer.buffer=_buffer;
    newBuffer.size=sizeBuf;
    return newBuffer;
}
*/
Index BufferByte::GetFileSize(std::string filename)
{
    FILE *fileIn;
    Index sizeFile;
    fileIn = fopen(filename.c_str(), "rb");
    if (!fileIn)
    {
        throw std::runtime_error("Unable to open file \"" + filename+"\" in Buffer::LoadBufferChunksFromFasta");
    }
    fseek(fileIn, 0, SEEK_END);
    sizeFile=ftell(fileIn);
    fclose(fileIn);
    return sizeFile;
}
