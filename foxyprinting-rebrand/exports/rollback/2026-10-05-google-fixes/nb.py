# usage: python3 nb.py [done_batch_no]  -> marks batch done, prints next pending batch
import json,sys
S='/tmp/claude-0/-home-user-panda/b27c821e-842d-5652-8996-b16be4651f6f/scratchpad'
items=json.load(open(f'{S}/phase2_items.json')); B=175
log=f'{S}/phase2_done.log'
if len(sys.argv)>1:
    open(log,'a').write(sys.argv[1]+'\n')
import shutil; shutil.copy(log,'/home/user/panda/foxyprinting-rebrand/exports/rollback/2026-10-05-google-fixes/phase2_done.log')
done={int(x) for x in open(log).read().split()}
n=(len(items)+B-1)//B
pend=[i for i in range(n) if i not in done]
print(f'done {len(done)}/{n}')
if not pend: print('ALL DONE'); sys.exit()
b=pend[0]; chunk=items[b*B:(b+1)*B]
print('BATCH',b)
for j in range(0,len(chunk),25):
    part=chunk[j:j+25]
    groups={}
    for pid,k,v in part: groups.setdefault(k+'='+v,[]).append(pid)
    print(f'a{j//25}: '+' | '.join(f'{g}: '+' '.join(ids) for g,ids in groups.items()))
