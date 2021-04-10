import json
from pprint import pprint
import numpy as np
with open('asrOutput (6).json', 'r', encoding='utf-8') as f:
    file = json.load(f)

pprint(file)
pprint(file['results']['transcripts'][0]['transcript'])

confidence = []

for i in file['results']['items']:
    confidence.append(i['alternatives'][0]['confidence'])

arr = np.array(confidence, dtype=np.float64)
#print(arr.mean())
arr2 = np.delete(arr, np.where(arr == 0))
print(arr)
print(arr2.mean())
