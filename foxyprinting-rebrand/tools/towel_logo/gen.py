"""Build GraphQL for the towel logo re-upload.
  gen.py staged <mid>...            -> stagedUploadsCreate mutation
  gen.py create <put.log lines>     -> productCreateMedia mutation (stdin: mid code resourceUrl)
  gen.py finish                     -> reorder + detach mutation (stdin: mid new_media_id); appends log.csv"""
import sys, json, re, os
HERE = os.path.dirname(os.path.abspath(__file__))
EXP = os.path.join(HERE, '..', '..', 'exports', 'towel-logo-removal-2026-10-09')
items = json.load(open(os.path.join(EXP, 'products.json')))
by_mid = {m['mid']: dict(i, pos=k) for i in items for k, m in enumerate(i['media'])}
q = json.dumps
LOWER = {'Retro', 'Football', 'Lightweight', 'Beach', 'Gym', 'Towel', 'Away', 'Goalkeeper', 'Third', 'Green', 'Yellow',
         'Cricket', 'World', 'Cup'}

def title(mid): return re.sub(r'\s+', ' ', by_mid[mid]['title']).strip()
def fname(mid):
    t = title(mid).lower().replace('lightweight beach gym towel', 'beach towel')
    return re.sub(r'[^a-z0-9]+', '-', t).strip('-') + '.jpg'
def alt(mid):
    return ' '.join(w.lower() if w in LOWER else w for w in title(mid).split()) + ' laid out on the sand'

cmd = sys.argv[1]
if cmd == 'staged':
    ins = ','.join(f'{{resource:IMAGE, filename:{q(fname(m))}, mimeType:"image/jpeg", httpMethod:PUT}}' for m in sys.argv[2:])
    print(f'mutation {{ stagedUploadsCreate(input:[{ins}]) {{ stagedTargets {{ url }} userErrors {{ field message }} }} }}')
elif cmd == 'create':
    out = []
    for n, line in enumerate(l for l in sys.stdin if l.strip()):
        mid, code, url = line.split()
        assert code == '200', line
        p = by_mid[mid]
        out.append(f'c{mid}: productCreateMedia(productId:"gid://shopify/Product/{p["pid"]}", media:[{{originalSource:{q(url)}, '
                   f'alt:{q(alt(mid))}, mediaContentType:IMAGE}}]) {{ media {{ id status }} mediaUserErrors {{ field message }} }}')
    print('mutation { ' + '\n'.join(out) + ' }')
elif cmd == 'finish':
    ops, files, log = [], [], []
    for line in (l for l in sys.stdin if l.strip()):
        mid, new = line.split()
        p = by_mid[mid]; P = f'gid://shopify/Product/{p["pid"]}'
        ops.append(f'r{mid}: productReorderMedia(id:{q(P)}, moves:[{{id:"gid://shopify/MediaImage/{new}", newPosition:"{p["pos"]}"}}]) '
                   f'{{ job {{ id }} mediaUserErrors {{ field message }} }}')
        files.append(f'{{id:"gid://shopify/MediaImage/{mid}", referencesToRemove:[{q(P)}]}}')
        log.append(f'{p["handle"]},{mid},{new},replaced')
    ops.append(f'd: fileUpdate(files:[{",".join(files)}]) {{ files {{ id fileStatus }} userErrors {{ field message }} }}')
    print('mutation { ' + '\n'.join(ops) + ' }')
    open(os.path.join(EXP, 'pending_log.csv'), 'w').write('\n'.join(log) + '\n')
