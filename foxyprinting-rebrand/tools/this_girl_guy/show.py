import json,sys
b=json.load(open(f'batches/{int(sys.argv[1]):03d}.json'))
print(b['query']); print(json.dumps(b['variables'],ensure_ascii=False,separators=(',',':')))
