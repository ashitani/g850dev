ORG 0x100

ld hl,hello_text    ; 文字
ld b,12             ; 文字数
ld d,3              ; yカーソル座標
ld e,0              ; xカーソル座標
call 0xbff1         ; 文字列表示
ret

hello_text:
defb "Hello, World"