#!/bin/sh
echo "loading:"
sigrok-cli --driver fx2lafw --config samplerate=20k -O bits:width=64 --channels=D0 --time 30s -o data.txt
echo "decoding:"
python decode.py data.txt
