#include <stdio.h>
#include <conio.h>

int inc(unsigned char *p) __z88dk_fastcall __naked {
#asm
    ld a,(hl)
    inc a
    ld (hl),a
    ret
#endasm
}

int main() {
  unsigned char a=10;

  clrscr(); // clear screen

  inc(&a);
  printf("%d\n", a);
}