.Phony: clean tests test

LIBS = -lboost_filesystem -lboost_system -lboost_program_options

CXXFLAGS = -Wall -std=c++14 -O3 -ggdb3 -g3 -fdiagnostics-color=auto -fopenmp -Wno-error=narrowing

all: bin/BNC_to_text bin/get_cooccurence_from_dir bin/sparse


bin/BNC_to_text: src/BNC_to_text.cpp
	g++  $^ $(CXXFLAGS) -o $@ $(LIBS)

bin/get_cooccurence_from_dir: obj/get_cooccurence_from_dir.o obj/buffer_byte.o obj/ternary_tree.o obj/vocabulary.o obj/stream_reader.o obj/string_tools.o
	g++  $^ $(CXXFLAGS) -o $@ $(LIBS)

obj/get_cooccurence_from_dir.o: src/get_cooccurence_from_dir.cpp 
	g++  $^ $(CXXFLAGS) -c -o $@ 

obj/vocabulary.o: src/vocabulary.cpp
	g++  $^ $(CXXFLAGS) -c -o $@ 

obj/string_tools.o: src/string_tools.cpp
	g++  $^ $(CXXFLAGS) -c -o $@ 

obj/buffer_byte.o: src/basic_utils/buffer_byte.cpp
	g++  $^ $(CXXFLAGS) -c -o $@ 

obj/stream_reader.o: src/basic_utils/stream_reader.cpp
	g++  $^ $(CXXFLAGS) -c -o $@ 

obj/ternary_tree.o: src/ternary_tree.cpp
	g++  $^ $(CXXFLAGS) -c -o $@ 

bin/sparse: src/sparse.cpp
	g++  $^ $(CXXFLAGS) -o $@ $(LIBS)

#tests
tests: bin/test_vocab

bin/test_vocab: src/tests/test_vocab.cpp obj/ternary_tree.o obj/vocabulary.o obj/stream_reader.o obj/string_tools.o
	g++  $^ $(CXXFLAGS) -o $@ $(LIBS)


test: all
	./bin/get_cooccurence_from_dir ./dirtest/test_minimal/ /tmp --minimal_frequency 1
	cat /tmp/frequencies
	echo
	./bin/get_cooccurence_from_dir ../data/test_corpora/rus/sep /tmp --minimal_frequency 1
	cat /tmp/frequencies

clean:
	rm -f obj/*.o
