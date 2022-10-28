#!bin/bash

## run in ./raw directory
for ff in *.nc
    do 
        echo $ff
        ncks -d time,0,2519 $ff ../summer/summer_$ff
    done
