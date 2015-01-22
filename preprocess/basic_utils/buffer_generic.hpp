#ifndef GENERIC_BUFFER
#define GENERIC_BUFFER

#include <iostream>
typedef int64_t Index;

#include "types.hpp"


template <typename T>
class GenericBuffer
{
public:
    std::string name;
	Index size;
	int * refCount;
	T * buffer; //todo: move to private
	GenericBuffer():size(0),buffer(NULL)
	{
        refCount=new int();
        *refCount=1;
	}

    GenericBuffer(const GenericBuffer &source)
    {
     //   std::cerr<<"copying buffer\n";
        buffer=source.buffer;
        size=source.size;
        name=source.name;
        refCount=source.refCount;
        (*refCount)++;

	}
	GenericBuffer & operator = (const GenericBuffer &source)
	{
     //   std::cerr<<"assigning buffer\n";

        if (this != &source) // protect against invalid self-assignment
        {
            buffer=source.buffer;
            size=source.size;
            refCount=source.refCount;
            name=source.name;
            (*refCount)++;
        }   // by convention, always return *this
        return *this;
	}

	virtual ~GenericBuffer()
	{
	    if (refCount==NULL) {std::cerr<<"Ref counter was not  set!!!!!\n";}
	    (*refCount)--;   // todo should be thread-safe
	//	std::cerr<<"destructing buffer "<<name<<", ref count="<<*refCount<<std::endl;
        if (*refCount==0)
        {
            if (buffer!=NULL) {delete[] buffer;}
            else
            {
                std::cerr<<"~Buffer: buffer was not allocated!!!";
            }
         //   std::cerr<<"redf count pointer:" << refCount<<std::endl;
            delete refCount;
            buffer=NULL;
            refCount=NULL;
        }
//        std::cerr<<"destructing buffer "<<name<<std::endl;


		#ifdef PRINT_ALL
        std::cout<<"destructing buffer"<<std::endl;
		#endif
	}

};

#endif
