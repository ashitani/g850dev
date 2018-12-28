#include <stdio.h>
#include <conio.h>

int add(int x,int y){
#asm
    ld ix,2
    add ix, sp

    ld h, (ix+3)  ;x_H
    ld l, (ix+2)  ;x_L
    ld b, (ix+1)  ;y_H
    ld c, (ix)    ;y_L
    add hl,bc
    ret
#endasm
}

int main() {
  clrscr(); // clear screen
  printf("%d\n", add(300,500));
}