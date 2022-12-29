import json


def parse(data,data_type):
	parseData = {}
	for entry in data:
		key = (entry['duration']//100)*100
		with open(f'raw_logs/{data_type}_{key}') as f:
			entry['gc'] = {}
			gc_times= list(map(float,f.read().replace('\n', '').split(',')))
			entry['gc']['avg'] = sum(gc_times)/len(gc_times)
			entry['gc']['sum'] = sum(gc_times)
		parseData[key] = entry
	return parseData


op_data = json.load(open('raw_logs/object-pooling.json'))
parsed_op_data = parse(op_data, 0)
with open('parsed_op_data.json', 'w+') as f:
	json.dump(parsed_op_data, f)

gc_data = json.load(open('raw_logs/garbage-collection.json'))
parsed_gc_data = parse(gc_data, 1)
with open('parsed_gc_data.json', 'w+') as f:
	json.dump(parsed_gc_data, f)

