CC = gcc
CXX = g++
#Using -Ofast instead of -O3 might result in faster code, but is supported only by newer GCC versions
LIBS = -lboost_filesystem -lboost_system -lm -pthread

CFLAGS =  $(LIBS) -O3 -march=native -Wall -funroll-loops -Wno-unused-result -std=c++14 -ggdb3 -g3 -fdiagnostics-color=auto 
CXXFLAGS = $(CFLAGS) -std=c++14 

all: word2vec word2phrase distance word-analogy compute-accuracy

word2vec : word2vec.cpp
	$(CXX) word2vec.cpp -o word2vec $(CFLAGS)

word2phrase : word2phrase.c
	$(CC) word2phrase.c -o word2phrase $(CFLAGS)

distance : distance.cpp
	$(CXX) distance.cpp -o distance $(CXXFLAGS)
word-analogy : word-analogy.c
	$(CC) word-analogy.c -o word-analogy $(CFLAGS)
compute-accuracy : compute-accuracy.c
	$(CC) compute-accuracy.c -o compute-accuracy $(CFLAGS)
	chmod +x *.sh

clean:
	rm -rf word2vec word2phrase distance word-analogy compute-accuracy