#!/bin/bash
sid=$1
start_year=2015
end_year=2015

if [ [$2] ]; then start_year=$2
fi

if [ [$3] ]; then end_year=$3
fi

file=./info/${sid}.info


if [ ! -f "$file" ]; then
  echo 'staion row index file not found!'
  ./gen_meta.py $sid
fi

for((i=start_year;i<=end_year;i++))
  do ./graph_generator.py $sid $i && ./analyzer.py $sid $i;

done


