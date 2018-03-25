/*
**  Author: Hao CHENG
**  Date: 15th Mar 2018
**  Description: Attack geffe-like stream cipher
*/

#include <iostream>
#include <armadillo>
#include <string>
#include <math.h>

using namespace std;
using namespace arma;

#define DIM 16

//taps of 3 LFSRs
int TAPS_L0[4] = {0, 1, 4, 7};
int TAPS_L1[4] = {0, 1, 7, 11};
int TAPS_L2[4] = {0, 2, 3, 5};

//Correct LFSR strings

char sequence_k1[200] = "";
char sequence_k2[200] = "";

string stream = "00100111111001010110111101100100110111110110111001110011000010010100000100001101110010010100110011001101011000110100100010011100001011001000111111011000001010101000000010100001001101111111100000011011";

//initialize 3 transfer matrixs of 3 LFSRs
mat T_L0(DIM, DIM, fill::zeros);
mat T_L1(DIM, DIM, fill::zeros);
mat T_L2(DIM, DIM, fill::zeros);

//initialize 3 key vectors
vec Key_L0(DIM,fill::zeros);
vec Key_L1(DIM,fill::zeros);
vec Key_L2(DIM,fill::zeros);


//Function: initialize the matrix T
mat Initialize_MatT(mat T, int taps[]){

  for(int i = 0; i < DIM - 1; i++){
      T(i, i + 1) = 1;
  }
  // add 4 taps to get the final T
  for (int i = 0; i < 4; i++){
  T(DIM - 1 , taps[i]) = 1;
  }
  return T;

}


//Function: get 16 bits output of LFSR
vec Get_LFSR_Out(mat T, vec Input){

  //From the start, with each 16 bits the state will be the output sequence.
  mat Tep(DIM, DIM, fill::zeros);
  vec Output(DIM, fill::zeros);
  vec S(DIM, fill::zeros);

  for (int i = 0; i < 4; i++){
    Tep = T * T;
    for(int i = 0; i < DIM; i++){
      for (int j = 0; j < DIM; j++){
        T(i, j) = int(Tep(i, j)) % 2 ;
      }
    }
  }
  Output = T * Input;
  return Output;

}


//Function: get the sequence from the key
void Get_Sequence(mat T, vec Key, char* sequence){

  vec Tmp_Vec(DIM, fill::zeros);
  Tmp_Vec = Key;

  for (int i = 0; i < 200; i++){
    // initialize first 16 bits
    if (i < DIM) sequence[i] = int(Key(i)) + '0';
    // every 16 bits , get more sequence
    else if (i % 16 == 0){
      Tmp_Vec = Get_LFSR_Out(T, Tmp_Vec);
      for (int j = i; (j < i + 16) && (j < 200); j++)
      sequence[j] = int(Tmp_Vec(j % 16)) % 2 + '0';
    }
  }
}


//Function: get the correlation between two streams
float Correlation(char* sequence, string keystream){

  int count = 0;
  float cor;
  for(int i = 0; i < 200; i++){
    if(sequence[i] == keystream[i]) count++;
  }
  cor = count / 200.0;
  return cor;

}


//Function: attack LFSR to get correct key
vec Attack_LFSR(mat T_L, vec Key_L, char* sequence_L){

  vec Key_Correct(DIM, fill::zeros);
  float cor = 0;
  for (int i = 0 ; i < pow(2,DIM); i++) {
      int tmp = i;
      for(int j = 0; j < DIM; j++){
        Key_L(j) = tmp % 2;
        tmp = tmp / 2;
      }

    Get_Sequence(T_L, Key_L, sequence_L);
    cor = Correlation(sequence_L, stream);
    if ( abs(cor - 0.75) < 0.02 ) {
      Key_Correct = Key_L;
      break;
    }
  }
  return Key_Correct;

}


//Function: whether the k0 is what I need
bool Is_Sequence_K0(char S_1[], char S_2[], string S_S, char S_0[]){

  string table = "01010011";
  int s1_int, s2_int, s0_int;
  for(int i = 0; i < 199; i++){
     s1_int = S_1[i] - '0';
     s2_int = S_2[i] - '0';
     s0_int = S_0[i] - '0';
     if (table[4 * s0_int + 2 * s1_int + s2_int] == S_S[i]) continue;
     else return false;
  }
  return true;

}


//Function: attack LFSR_0 to get the correct key_l0
vec Attack_LFSR_0(mat T_L, vec Key_L){

  vec Key_Correct(DIM, fill::zeros);

  for (int i = 0 ; i < pow(2,DIM); i++) {
      char sequence_L[200] = "";
      int tmp = i;
      for(int j = 0; j < DIM; j++){
        Key_L(j) = tmp % 2;
        tmp = tmp / 2;
      }
    Get_Sequence(T_L, Key_L, sequence_L);

    if(Is_Sequence_K0(sequence_k1, sequence_k2, stream, sequence_L)){
      Key_Correct = Key_L;
    }
  }
  return Key_Correct;
}


//Function: transform key from vector to string
void Trans_Key_Str(vec vector_p, char str_p[]){

  for (int i = 0; i < DIM; i++){
    str_p[i] = int(vector_p(i)) + '0';
  }
}


int main(){

  T_L0 = Initialize_MatT(T_L0, TAPS_L0);
  T_L1 = Initialize_MatT(T_L1, TAPS_L1);
  T_L2 = Initialize_MatT(T_L2, TAPS_L2);

  char key_l1[DIM];
  cout << "\nAttacking for the LFSR_1, please wait..." << endl;
  Key_L1 = Attack_LFSR(T_L1, Key_L1, sequence_k1);
  Trans_Key_Str(Key_L1, key_l1);
  cout << "The key of LFSR_1 is: " << key_l1 << endl;

  char key_l2[DIM];
  cout << "\nAttacking for the LFSR_2, please wait..." << endl;
  Key_L2 = Attack_LFSR(T_L2, Key_L2, sequence_k2);
  Trans_Key_Str(Key_L2, key_l2);
  cout << "The key of LFSR_2 is: " << key_l2 << endl;

  char key_l0[DIM];
  cout << "\nAttacking for the LFSR_0, please wait..." << endl;
  Key_L0 = Attack_LFSR_0(T_L0, Key_L0);
  Trans_Key_Str(Key_L0, key_l0);
  cout << "The key of LFSR_0 is: " << key_l0 << endl;

  cout<< "\nThe result of attack:" << endl;
  cout << "Key[k_0, k_1, k_2] = " << endl;
  cout << key_l0 << ", " << key_l1 << ", " << key_l2 << endl;

  return 0;

}
