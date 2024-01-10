#include "numbers.h"
#include "time.h"
#include "stdio.h"
#include <stdio.h>

int asm_max(int a, int b) {
  __asm__ volatile("CMP %w1, %w2;"             // Compare a and b
                   "BLT not_greater_than%=;" // Branch if less than (a < b)
                   "MOV %w0, %w1;"             // Move a to output registry
                   "B end_comparison%=;"
                   "not_greater_than%=:"
                   "MOV %w0, %w2;" // Move b to output registry
                   "end_comparison%=:"

                   : "=r"(a)   // Output operand (result)
                   : "r"(a), "0"(b) // Input operands (a, b)
  );
  return a;
}

/*
Internal min function
*/
int asm_min(int a, int b) {
  __asm__ volatile("CMP %w1, %w2;"             // Compare a and b
                   "BLT not_greater_than%=;" // Branch if less than (a < b)
                   "MOV %w0, %w2;"             // Move b to output registry
                   "B end_comparison%=;"
                   "not_greater_than%=:"
                   "MOV %w0, %w1;" // Move a to output registry
                   "end_comparison%=:"

                   : "=r"(a)   // Output operand (result)
                   : "r"(a), "0"(b) // Input operands (a, b)
  );
  return a;
}

/*
Internal max function
*/
int max(int a, int b) {
  if (a > b) {
    return a;
  }
  return b;
}

/*
Internal max function
*/
int min(int a, int b) {
  if (a < b) {
    return a;
  }
  return b;
}

int main() {
  clock_t begin = clock();
  for (int x = 0; x < 1000000; x++) {
    for (int i = 0; i < 64; i++) {
      min(numbers[i], numbers[63 - i]);
      max(numbers[i], numbers[63 - i]);
    }
  }
  clock_t end = clock();
  double time_spent = (double)(end - begin) / CLOCKS_PER_SEC;
  printf("No asm: %f\n", time_spent);

  begin = clock();
  for (int x = 0; x < 1000000; x++) {
    for (int i = 0; i < 64; i++) {
      asm_min(numbers[i], numbers[63 - i]);
      asm_max(numbers[i], numbers[63 - i]);
    }
  }
  end = clock();
  time_spent = (double)(end - begin) / CLOCKS_PER_SEC;
  printf("asm: %f\n", time_spent);
}