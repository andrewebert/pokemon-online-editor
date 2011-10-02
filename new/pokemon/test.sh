#!/bin/sh

for file in `ls *.txt`; do
    echo "===${file}==="
    diff ${file} ../../../pokes/${file}
done
