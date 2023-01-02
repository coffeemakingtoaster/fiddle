#! /bin/bash

benchmark() {
for i in {1..100}
do
	duration=$((i*100))
	echo Running for $duration ms
	node --trace_gc ./garbage-collection.js $1 $duration > log.txt
	parse_log "${1}_${duration}"
	rm log.txt
done
}

parse_log(){
	while read p;
	do
		gctype=$(echo $p | grep -o ': .* -> ' | grep -o '[a-zA-Z]*') 
		timing=$(echo $p | grep -o 'MB, .* /' | grep -o '[1-9]*\.[0-9]*')
		echo "${timing} ; ${gctype}">>"raw_logs/${1}"
	done < log.txt
}


echo 'Cleanup existing'
rm *.json
rm -R raw_logs
mkdir raw_logs
echo 'Benchmarking garbage collection'
benchmark 0

echo 'Benchmarking object pooling'
benchmark 1
