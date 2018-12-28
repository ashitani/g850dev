;http://d.hatena.ne.jp/tosik/20080312/1205295088
; 一文字表示
.area   _HEADER (ABS)
.ORG #0x100
ld a,#'a'    ; 文字a
ld d,#0      ; yカーソル座標
ld e,#0      ; xカーソル座標
call #0xbe62
ret
