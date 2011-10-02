#!/bin/sh

for file in `ls *.txt`; do
    echo "===${file}==="
    diff ${file} ../../../../moves/5G/${file}
done
