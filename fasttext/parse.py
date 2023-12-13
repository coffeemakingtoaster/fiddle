import json
import os
import sys
from collections import defaultdict

index = 0
buffer_size = 10_000

def def_val():
    return []


if __name__ == "__main__":

    with open("cc.de.300.vec", "r") as f:
        buffer =  defaultdict(def_val) 
        cnt = 0 
    
        for line in f:
            percent = (cnt/2000001) * 100
            print(f"{percent}% ({cnt}/2000001)", end="\r")
            values = line.split(" ")
            item = {
                "word": values[0],
                "embedding": [float(x) for x in values[1:]]
            }
            buffer[values[0][0]].append(item)
            if len(buffer[values[0][0]]) > buffer_size:
                data = [] 
                if os.path.exists(f"./words-{values[0][0]}.json"):
                    data = json.load(open(f"words-{values[0][0]}.json", "r"))
                # Write buffer and initial file contents
                with open(f"words-{values[0][0]}.json", "w+") as bf_f:
                    data += buffer[values[0][0]]
                    json.dump(data, bf_f)
                # Reset buffer
                buffer[values[0][0]] = []
            cnt += 1