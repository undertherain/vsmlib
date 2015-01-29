.Phony: clean run

LIBS = -lboost_filesystem -lboost_system

CXXFLAGS = -Wall -std=c++14 -O3 -ggdb3 -g3 -fdiagnostics-color=auto -fopenmp

all: test_tree test_reader

test_tree: test_tree.cpp
	g++  $^ $(CXXFLAGS) -o $@ $(LIBS)

test_reader: test_reader.cpp
	g++  $^ $(CXXFLAGS) -o $@ $(LIBS)

run: test_tree
	./test_tree
	dot -Tpng original.gv -o original.png
	dot -Tpng reduced.gv  -o reduced.png

clean:
	rm *.o