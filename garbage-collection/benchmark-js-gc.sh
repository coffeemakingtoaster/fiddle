#! /bin/bash

benchmark() {
for i in {1..100}
do
	duration=$((i*100))
	echo Running for $duration ms
	node --trace_gc ./garbage-collection.js $1 $duration > log.txt
	parse_log "${1}_${duration}"
done
}

parse_log(){
	targets=(`grep -o 'MB, .* /' log.txt | grep -o '[1-9]*\.[0-9]*' | cut -d',' -f1`)
	printf -v joined '%s,' "${targets[@]}"
	echo "${joined%,}">"raw_logs/${1}"
}


echo 'Cleanup existing'
rm *.json
rm -R raw_logs
mkdir raw_logs
echo 'Benchmarking garbage collection'
benchmark 0

echo 'Benchmarking object pooling'
benchmark 1
