#!/bin/bash

num_keys=5
num_gh_tokens=$(grep "NUM_GH_ACCESS_TOKENS" __global_paths.py | sed 's/.*= *\([0-9]*\)/\1/')


for (( start_key=0; start_key<=num_keys; start_key+=num_gh_tokens ));
do
	for (( key=start_key; key<start_key+num_gh_tokens && key<num_keys ; key++ ));
	do
		python3 3_get_bugs.py closed $key &
	done
	wait
done
