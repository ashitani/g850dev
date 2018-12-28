#include <graphics.h>
#include <math.h>
#include <stdio.h>

void main() {
  int x, y;
  clg();

  plot(0,24);
  for (x = 0; x < 144; x++) {
    y = (int)(24 * (1.0 - sin(x / 144.0 * 3.14 * 8)));
    drawto(x, y);
  }

  while (getk() != 10) {};
}