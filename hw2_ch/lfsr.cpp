/*
**  Author: Hao CHENG
**  Date: 13th Mar 2018
**  Description: LFSR
*/

#include <iostream>
#include <armadillo>

using namespace std;
using namespace arma;

//dimontion of the matrix and vector
#define DIM 128

int main(){

  //construct the T matrix S vector
  mat T(DIM, DIM, fill::zeros);
  mat Tep(DIM, DIM, fill::zeros);
  vec S(DIM, fill::ones);
  vec Sep(DIM, fill::zeros);

  for(int i = 0; i < DIM - 1; i++){
      T(i, i + 1) = 1;
  }

  // add taps to get the final T
  T(DIM - 1, 0) = 1;
  T(DIM - 1, 1) = 1;
  T(DIM - 1, 6) = 1;
  T(DIM - 1, 105) = 1;

  //get 64 times squre of T
  for (int i = 0; i < 64; i++){
    Tep = T * T;
    for(int i = 0; i < DIM; i++){
      for (int j = 0; j < DIM; j++){
        T(i, j) = int(Tep(i, j)) % 2 ;
      }
    }
  }

  char output[] = "";
  Sep = T * S;

  //get the final result
  for(int i = 0; i < DIM; i++){
  S[i] = int(Sep[i]) % 2;

  if(S[i]) output[i] = '1';
  else output[i] = '0';

}

  puts("\nFinal state of LFSR atfer 2^64 iterations:");
  puts(output);

  return 0;
}
