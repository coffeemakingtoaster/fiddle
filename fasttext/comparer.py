import json
import math
import sys
from operator import itemgetter


if __name__ == "__main__":
    word = sys.argv[1]
    print(f"Word: {word}")
    data = []
    related = [] 
    item_embedding = []
    with open(f"words-{word[0]}.json") as f:
        data = json.load(f)
    for item in data:
        if item["word"] == word:
            item_embedding = item["embedding"]
            continue
        if str(item["word"]).startswith(word):
            related.append(item)
    
    print(f"Found {len(related)} items")
    for item in related:
       item["distance"] = math.dist(item["embedding"], item_embedding)
    
    related.sort(key=itemgetter('distance'))
    
    print(f"For word {word} these are the top 10 by distance:")
    for i, v in enumerate(related[:10]):
        print(f"{i+1}.\t{v['word']}\t(Dist: {v['distance']})")
    