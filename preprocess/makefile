.Phony: clean
LIBS = -lboost_filesystem -lboost_system

CXXFLAGS = -Wall -std=c++14 -O3 -ggdb3 -g3 -fdiagnostics-color=auto -fopenmp

all: BNC_to_text get_cooccurence_from_dir sparse

BNC_to_text: BNC_to_text.cpp
	g++  $^ $(CXXFLAGS) -o $@ $(LIBS)

get_bigrams: get_bigrams.cpp
	g++  $^ $(CXXFLAGS) -o $@ $(LIBS)

get_bigrams_sort: get_bigrams_sort.cpp buffer_byte.o
	g++  $^ $(CXXFLAGS) -o $@ $(LIBS)

get_cooccurence_from_dir: get_cooccurence_from_dir.cpp buffer_byte.o
	g++  $^ $(CXXFLAGS) -o $@ $(LIBS)

get_frequency: get_frequency.cpp
	g++  $^ $(CXXFLAGS) -o $@ $(LIBS)

get_frequency_all: get_frequency_all.cpp
	g++  $^ $(CXXFLAGS) -o $@ $(LIBS)

get_frequency_tree: get_frequency_tree.cpp
	g++  $^ $(CXXFLAGS) -o $@ $(LIBS)

buffer_byte.o: basic_utils/buffer_byte.cpp
	g++  $^ $(CXXFLAGS) -c -o $@ $(LIBS)

sparse: sparse.cpp
	g++  $^ $(CXXFLAGS) -o $@ $(LIBS)


clean:
	rm *.o