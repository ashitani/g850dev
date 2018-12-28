# PC-G850V RAM拡張ボードと、それを用いた長編（動画）再生プロジェクト

詳細は[こちら](http://ashitani.jp/g850dev/10_ext_rom.html) を参照ください。

# blender

- spaceship.blender: 動画のblenderファイル

# images

- spaceship: 動画をレンダリングした画像ファイル
- spaceship_1bit: それを2値化した画像
- conv_1bit.py: 2値化のための変換スクリプト

# pcb

- ext_ram: 増設RAM拡張ボードのKiCadファイルです。バグが１箇所ありますが未修正です。[こちら](http://ashitani.jp/g850dev/10_ext_rom.html) を参照ください。
- lib: 部品等のライブラリです。

# src

PCからの動画転送、増設RAMへの書き込み、増設RAMからの動画再生、を行うコードです。

## ポケコン側のプログラム

- main.c: メインプログラム
- display.c: 圧縮伸張と表示のライブラリ
- extrom.c: 増設RAMの読み書きを行うライブラリ
- uart.c: PCとのUART通信を行うライブラリ

## PC側のプログラム

- transfer.py: 画像を圧縮してUART転送するプログラム。

UARTのデバイス、転送ファイル、メモリ領域などすべて決め打ちなので、
変更する場合はmain以下の修正が必要です。

