import json,sys,datetime
n=int(sys.argv[1]); status=sys.argv[2]; note=sys.argv[3] if len(sys.argv)>3 else ''
b=json.load(open(f'/tmp/claude-0/-home-user-panda/b27c821e-842d-5652-8996-b16be4651f6f/scratchpad/tgtg/batches/{n:03d}.json'))
with open('/home/user/panda/foxyprinting-rebrand/exports/this-girl-this-guy/2026-10-06-push-log.jsonl','a') as f:
    f.write(json.dumps({'batch':n,'status':status,'note':note,'product_ids':b['ids'],'at':datetime.datetime.utcnow().isoformat()+'Z'})+'\n')
