#ifndef MY_BUFFER
#define MY_BUFFER

#include <string>
#include <vector>

#include "buffer_generic.hpp"
//#include "basic_utils/exceptions.hpp"

Index LoadBytesFromFile(byte ** buffer,std::string nameFileIn);

class BufferByte:public GenericBuffer<byte>
{
private:
	Index distributionNucleotides[4];
	void Init();
protected:

public:
	BufferByte();
	BufferByte(std::string str);
	Index offsetChunk;
	virtual ~BufferByte();
	virtual byte & operator[](Index idx) const;
	virtual void Print() const;
	static Index GetFileSize(std::string filename);
	//static BufferByte LoadFromDir();
	static BufferByte LoadFromFile(std::string nameFileIn);
	bool less(Index l,Index r);
};
	
#endif
