.Phony: clean
LIBS = -lboost_filesystem -lboost_system -lboost_program_options

CXXFLAGS = -Wall -std=c++14 -O3 -ggdb3 -g3 -fdiagnostics-color=auto -fopenmp

all: bin/BNC_to_text bin/get_cooccurence_from_dir bin/sparse


bin/BNC_to_text: src/BNC_to_text.cpp
	g++  $^ $(CXXFLAGS) -o $@ $(LIBS)

bin/get_cooccurence_from_dir: src/get_cooccurence_from_dir.cpp obj/buffer_byte.o obj/ternary_tree.o
	g++  $^ $(CXXFLAGS) -o $@ $(LIBS)

obj/buffer_byte.o: src/basic_utils/buffer_byte.cpp
	g++  $^ $(CXXFLAGS) -c -o $@ 

obj/ternary_tree.o: src/ternary_tree.cpp
	g++  $^ $(CXXFLAGS) -c -o $@ 

bin/sparse: src/sparse.cpp
	g++  $^ $(CXXFLAGS) -o $@ $(LIBS)

clean:
	rm -f obj/*.o