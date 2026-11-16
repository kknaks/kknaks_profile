import json,sys
# usage: mkreq.py <n> <idempotency_key> <out> [patch.json]
D='/Users/kknaks/orca/workspaces/kknaks_profile/day-r3/orchestration/work/fix/delivery'
n,key,out=sys.argv[1],sys.argv[2],sys.argv[3]
i=json.load(open(f'{D}/{n}/issue-before.json')); c=i['contract']
r={"idempotency_key":key,"title":i['title'],"product_id":"day","document_root":"products/day",
 "contract_version":c['contract_version']+1,"risk_level":c['risk_level'],"target_specs":c['target_specs'],
 "spec_baseline_revision":"19f7e40183e9cdb673db89190b831094507901a4",
 "target_delta":c['target_delta'],"acceptance":c['acceptance'],"non_goals":c['non_goals'],"review_surface":c['review_surface']}
if len(sys.argv)>4:
    p=json.load(open(sys.argv[4])); r.update(p)
json.dump(r,open(out,'w'),ensure_ascii=False,indent=2)
