.Phony: clean
LIBS = -lboost_filesystem -lboost_system

CXXFLAGS = -Wall -std=c++14 -O3 -ggdb3 -g3
all: BNC_to_text get_bigrams get_bigrams_sort get_frequency get_frequency_all

BNC_to_text: BNC_to_text.cpp
	g++  $^ $(CXXFLAGS) -o $@ $(LIBS)

get_bigrams: get_bigrams.cpp
	g++  $^ $(CXXFLAGS) -o $@ $(LIBS)

get_bigrams_sort: get_bigrams_sort.cpp buffer_byte.o
	g++  $^ $(CXXFLAGS) -o $@ $(LIBS)

get_frequency: get_frequency.cpp
	g++  $^ $(CXXFLAGS) -o $@ $(LIBS)

get_frequency_all: get_frequency_all.cpp
	g++  $^ $(CXXFLAGS) -o $@ $(LIBS)

buffer_byte.o: basic_utils/buffer_byte.cpp
	g++  $^ $(CXXFLAGS) -c -o $@ $(LIBS)

clean:
	rm *.o