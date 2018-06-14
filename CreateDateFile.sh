#! /bin/bash

OUT_FILE=,date.txt
rm -f $OUT_FILE


IN_FILES=,*.txt
echo $IN_FILES

cat $IN_FILES | grep -Pe '^\d{4}-\d{2}-\d{2}' | awk '{print $1}' | sort | uniq > $OUT_FILE
