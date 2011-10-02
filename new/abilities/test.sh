#!/bin/sh

for file in `ls *.txt`; do
    echo "===${file}==="
    diff ${file} ../../../abilities/${file}
done
