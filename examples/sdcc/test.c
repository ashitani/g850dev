void putc(char c,char x,char y){
    __asm
    ld ix,#2
    add ix,sp
    ld      a,0(ix)      ; character
    ld      e,1(ix)      ; x cursor
    ld      d,2(ix)      ; y cursor
    call #0xbe62         ; call IOCS
    __endasm;
}

void main()
{
    putc('a',3,3);
}