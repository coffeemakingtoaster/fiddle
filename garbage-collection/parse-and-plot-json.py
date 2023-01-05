import json
import matplotlib.pyplot as plt 
from collections import defaultdict

def plot(parsed_gc_data, parsed_op_data):
	times = (list(parsed_gc_data.keys()))
	times.sort()
	creationPerMsGC = [parsed_gc_data[key]['createdPerMs'] for key in times ]
	creationPerMsOP = [parsed_op_data[key]['createdPerMs'] for key in times ]
	gc_breakdown_dict = defaultdict(float)
	for key in times:
		bd = parsed_gc_data[key]['gc']['breakdown']
		for k in bd.keys():
			gc_breakdown_dict[k] += float(bd[k])
	op_breakdown_dict = defaultdict(float)
	for key in times:
		bd = parsed_op_data[key]['gc']['breakdown']
		for k in bd.keys():
			op_breakdown_dict[k] += float(bd[k])

	# Export creation per ms plot
	plt.figure()
	plt.plot(times, creationPerMsGC, label='ohne Object Pooling')
	plt.plot(times, creationPerMsOP, label='mit Object Pooling')
	plt.xlabel('Testdauer in ms')
	plt.ylabel('Erstellte Objekte pro ms')
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
	plt.xticks([0,1], ['Ohne Object Pooling', 'Mit Object Pooling'])
	plt.ylabel('Garbage-Collection Dauer in s')
	plt.savefig('exports/compare_time_spent_with_gc')
	# Export total objects created
	plt.figure()
	gc_createdObjects_sum = sum([parsed_gc_data[key]['totalCount'] for key in times ])/1_000_000
	op_createdObjects_sum = sum([parsed_op_data[key]['totalCount'] for key in times ])/1_000_000
	bars = plt.bar([0,1],[gc_createdObjects_sum, op_createdObjects_sum])
	bars[0].set_color('#1f77b4')
	bars[1].set_color('#ff7f0e')
	plt.xticks([0,1], ['ohne Object Pooling', 'mit Object Pooling'])
	plt.ylabel('Summe an erstellten Objekten (in Millionen)')
	plt.savefig('exports/compare_objects_created_total')
	# Export gc distribution gc
	plt.figure()
	plt.title('Zeit pro Garbage Collection Algorithmus in s (ohne Object Pooling)')
	plt.pie(gc_breakdown_dict.values(), labels=gc_breakdown_dict.keys(), autopct=lambda p : '{:.2f}%  ({:,.0f})'.format(p,p * sum(gc_breakdown_dict.values())/100))
	plt.savefig('exports/gc_gc_breakdown')
	# Export gc distribution op 
	plt.figure()
	plt.title('Zeit pro Garbage Collection Algorithmus in s (mit Object Pooling)')
	plt.pie(op_breakdown_dict.values(), labels=op_breakdown_dict.keys(), autopct=lambda p : '{:.2f}%  ({:,.0f})'.format(p,p * sum(op_breakdown_dict.values())/100))
	plt.savefig('exports/op_gc_breakdown')



	


def parse(data,data_type):
	key = 100 
	parseData = {}
	for entry in data:
		with open(f'raw_logs/{data_type}_{key}') as f:
			gc_times = []
			gc_breakdown = defaultdict(float)
			lines = f.readlines()
			for line in lines:
				line = line.replace('\n', '')
				if line != 'Compact':
					dur, gc_type = line.split(';')
					gc_times.append(float(dur))
					if gc_type == "Mark":
						gc_type += "Compact"
					gc_breakdown[gc_type] += float(dur)
			entry['gc'] = {}
			entry['gc']['avg'] = sum(gc_times)/len(gc_times)
			entry['gc']['sum'] = sum(gc_times)
			entry['gc']['breakdown'] = gc_breakdown
		parseData[key] = entry
		key+=100
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

