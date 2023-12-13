import json
import os
import sys
from collections import defaultdict

MAX_BUFFER_SIZE_PER_KEY = 100_000

def def_val():
    return []

def dump(key, val):
    data = [] 
    if os.path.exists(f"./words-{key}.json"):
        data = json.load(open(f"words-{values[0][0]}.json", "r"))
    # Write buffer and initial file contents
    # This is slow...string manipulation would probably be faster
    with open(f"words-{key}.json", "w+") as bf_f:
        data += val 
        json.dump(data, bf_f)

if __name__ == "__main__":
    buffer =  defaultdict(def_val) 
    cnt = 0 

    with open("cc.en.300.vec", "r") as f:
    
        for line in f:
            percent = (cnt/2000001) * 100
            print(f"{percent}% ({cnt}/2000001)", end="\r")
            values = line.split(" ")
            item = {
                "word": values[0],
                "embedding": [float(x) for x in values[1:]]
            }
            buffer[values[0][0]].append(item)
            if len(buffer[values[0][0]]) > MAX_BUFFER_SIZE_PER_KEY:
                dump(values[0][0], buffer[values[0][0]])
                # Reset buffer
                buffer[values[0][0]] = []
            cnt += 1

    print("Tidying up...")
    for key in buffer.keys():
        # If buffer for key is empty then skip
        if len(buffer[key]) == 0:
            continue
        dump(key, buffer[key])