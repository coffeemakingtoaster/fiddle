import json
import matplotlib.pyplot as plt 


def plot(parsed_gc_data, parsed_op_data):
	times = (list(parsed_gc_data.keys()))
	times.sort()
	creationPerMsGC = [parsed_gc_data[key]['createdPerMs'] for key in times ]
	creationPerMsOP = [parsed_op_data[key]['createdPerMs'] for key in times ]
	# Export creation per ms plot
	plt.figure()
	plt.plot(times, creationPerMsGC, label='Garbage Colletion')
	plt.plot(times, creationPerMsOP, label='Object Pooling')
	plt.xlabel('Testdauer in Millisekunden')
	plt.ylabel('Erstellte Objekte pro Millisekunde')
	plt.legend()
	plt.savefig(f'exports/compare_creation_per_ms')
	plt.close()
	# Export time spent with gc plot
	plt.figure()
	gc_gc_sum = sum([parsed_gc_data[key]['gc']['sum'] for key in times ])/1000
	op_gc_sum =  sum([parsed_op_data[key]['gc']['sum'] for key in times ])/1000
	bars = plt.bar([0,1],[gc_gc_sum, op_gc_sum])
	bars[0].set_color('#1f77b4')
	bars[1].set_color('#ff7f0e')
	plt.xticks([0,1], ['Garbage collection', 'Object Pooling'])
	plt.ylabel('Garbage-Collection Dauer in Sekunden')
	plt.savefig('exports/compare_time_spent_with_gc')
	# Export total objects created
	plt.figure()
	gc_createdObjects_sum = sum([parsed_gc_data[key]['totalCount'] for key in times ])/1_000_000
	op_createdObjects_sum = sum([parsed_op_data[key]['totalCount'] for key in times ])/1_000_000
	bars = plt.bar([0,1],[gc_createdObjects_sum, op_createdObjects_sum])
	bars[0].set_color('#1f77b4')
	bars[1].set_color('#ff7f0e')
	plt.xticks([0,1], ['Garbage collection', 'Object Pooling'])
	plt.ylabel('Summe an erstellten Objekten (in Millionen)')
	plt.savefig('exports/compare_objects_created_total')



	


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
parsed_op_data = parse(op_data, 1)
with open('parsed_op_data.json', 'w+') as f:
	json.dump(parsed_op_data, f)

gc_data = json.load(open('raw_logs/garbage-collection.json'))
parsed_gc_data = parse(gc_data, 0)
with open('parsed_gc_data.json', 'w+') as f:
	json.dump(parsed_gc_data, f)
plot(parsed_gc_data, parsed_op_data)

