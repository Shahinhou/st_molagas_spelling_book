#!/bin/sh

for s in $(cat 'nums.txt')
do
    #echo $s
    cat -n 'unique_criteria_list.txt' | grep -w $s
done
