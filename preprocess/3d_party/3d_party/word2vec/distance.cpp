#include <stdexcept>
#include <iostream>
#include <stdio.h>
#include <string.h>
#include <math.h>
#include <malloc.h>
#include "../string_tools.hpp"

const long long max_size = 2000;         // max length of strings
const long long cnt_results = 10;                  // number of closest words that will be shown
const long long max_w = 50;              // max length of vocabulary entries

long long size_vocavulary, size_vector;
char *vocab;

void normalize_vec(float * vec, const int64_t size)
{
    float norm = 0;
    for (int64_t i = 0; i < size; i++) 
    	norm += vec[i] * vec[i];
    norm = sqrt(norm);
    for (int64_t i = 0; i < size; i++) 
    	vec[i] /= norm;
}

void load_matrix(char * file_name, float * & M)
{
  FILE *f;
  long long a;
  f = fopen(file_name, "rb");
  if (f == NULL) {
    printf("Input file not found\n");
    throw std::runtime_error("Cannot open file: in load matrix");
  }
  fscanf(f, "%lld", &size_vocavulary);
  fscanf(f, "%lld", &size_vector);
  vocab = (char *)malloc((long long)size_vocavulary * max_w * sizeof(char));
  M = (float *)malloc((long long)size_vocavulary * (long long)size_vector * sizeof(float));
  if (M == NULL) {
    printf("Cannot allocate memory: %lld MB    %lld  %lld\n", (long long)size_vocavulary * size_vector * sizeof(float) / 1048576, size_vocavulary, size_vector);
    throw std::runtime_error("Cannot allocate memory: in load matrix");
  }
  for (int64_t id_word = 0; id_word < size_vocavulary; id_word++) {
    a = 0;
    while (1) {
      vocab[id_word * max_w + a] = fgetc(f);
      if (feof(f) || (vocab[id_word * max_w + a] == ' ')) break;
      if ((a < max_w) && (vocab[id_word * max_w + a] != '\n')) a++;
    }
    vocab[id_word * max_w + a] = 0;
    fread(&M[id_word * size_vector], sizeof(float), size_vector, f);
	normalize_vec(&M[id_word * size_vector],size_vector);
  }
  fclose(f);
}

char * get_word_by_id(int64_t id)
{
  if (id<0)  return NULL;

  return (&vocab[id * max_w]);
}

int64_t get_word_id(const char * word)
{
  for (int64_t i = 0; i < size_vocavulary; i++) if (!strcmp(&vocab[i * max_w], word)) return i;
  return -1;
}

void print_most_similar(float * & M,int cnt_tokens,long long * bi)
{
  int64_t best_pos[cnt_results];
  float dist, len, best_dist[cnt_results], vec[max_size];
 // long long bi[100];
  int64_t a,b,c,d;
  for (int64_t i = 0; i < cnt_results; i++) best_dist[i] = 0;

   // printf("\n                          Word          Cosine distance\n-------------------------------------------------------\n");
    for (a = 0; a < size_vector; a++) vec[a] = 0;
    for (b = 0; b < cnt_tokens; b++) {
      if (bi[b] == -1) continue;
      for (a = 0; a < size_vector; a++) vec[a] += M[a + bi[b] * size_vector];
    }
    len = 0;
    for (a = 0; a < size_vector; a++) len += vec[a] * vec[a];
    len = sqrt(len);
    for (a = 0; a < size_vector; a++) vec[a] /= len;
    for (a = 0; a < cnt_results; a++) best_dist[a] = -1;
    for (c = 0; c < size_vocavulary; c++) {
      a = 0;
      for (b = 0; b < cnt_tokens; b++) if (bi[b] == c) a = 1;
      if (a == 1) continue;
      dist = 0;
      for (a = 0; a < size_vector; a++) dist += vec[a] * M[a + c * size_vector];
      for (a = 0; a < cnt_results; a++) {
        if (dist > best_dist[a]) {
          for (d = cnt_results - 1; d > a; d--)
          {
            best_dist[d] = best_dist[d - 1];
            best_pos[d]= best_pos[d-1];
          }
          best_dist[a] = dist;
          best_pos[a] = c;
          break;
        }
      }
    }
    for (int64_t i = 0; i < cnt_results; i++) printf("%30s\t-\t%f\n", get_word_by_id(best_pos[i]), best_dist[i]);

}


int main(int argc, char **argv) {
  char str_input[max_size];
  char file_name[max_size], tokens_strs[100][max_size];
  //float vec[max_size];
  long long a, b, c, cnt_tokens, tokens_ids[100];
  //char ch;
  float *M;
  if (argc < 2) {
    printf("Usage: ./distance <FILE>\nwhere FILE contains word projections in the BINARY FORMAT\n");
    return 0;
  }
  strcpy(file_name, argv[1]);
  load_matrix(file_name,M);

  while (1) {
    printf("Enter word or sentence (EXIT to break): ");
    a = 0;
    while (1) {
      str_input[a] = fgetc(stdin);
      if ((str_input[a] == '\n') || (a >= max_size - 1)) {
        str_input[a] = 0;
        break;
      }
      a++;
    }
    if (!strcmp(str_input, "EXIT")) break;
    cnt_tokens = 0;
    b = 0;
    c = 0;
    while (1) {
      tokens_strs[cnt_tokens][b] = str_input[c];
      b++;
      c++;
      tokens_strs[cnt_tokens][b] = 0;
      if (str_input[c] == 0) break;
      if (str_input[c] == ' ') {
        cnt_tokens++;
        b = 0;
        c++;
      }
    }
    cnt_tokens++;
    for (a = 0; a < cnt_tokens; a++) {
      b=get_word_id(tokens_strs[a]);
      if (b == size_vocavulary) b = -1;
      tokens_ids[a] = b;
      printf("\nWord: %s  Position in vocabulary: %lld\n", tokens_strs[a], tokens_ids[a]);
      if (b == -1) {
        printf("Out of dictionary word!\n");
        break;
      }
    }
    if (b == -1) continue;
    print_most_similar(M,cnt_tokens,tokens_ids);
  }
  std::string str = "test";
  auto wordlist=load_words("../words_of_interest.txt");
  //for (auto i: wordlist)
  //{
//    std::cout << "\nmost similar rows to *"<< i <<"* are: \n";
    //long long int id= get_word_id(i.c_str());
    //print_most_similar(M,1,&id);
  //}
  return 0;
}
