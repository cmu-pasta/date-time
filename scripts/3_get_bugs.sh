#!/bin/bash

num_keys=5
num_gh_keys=6

for (( start_key=0; start_key<=num_keys; start_key+=num_gh_keys ));
do
	for (( key=start_key; key<start_key+num_gh_keys && key<num_keys ; key++ ));
	do
		python3 3_get_bugs.py closed $key $num_gh_keys &
	done
	wait
done
