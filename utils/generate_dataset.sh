#!/bin/bash

# Generate $1 different circuits with each $2 faults

for (( i=0; i<$1 ; i++ ))
do
    make test
done