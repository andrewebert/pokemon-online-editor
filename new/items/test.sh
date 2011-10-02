#!/bin/sh

for file in `ls *.txt`; do
    echo "===${file}==="
    diff ${file} ../../../items/${file}
done
