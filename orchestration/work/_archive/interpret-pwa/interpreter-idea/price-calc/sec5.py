"""price.md 5절 — 2만 원 기준 1단위 원가 × 마진 30~70%. 원가 단위 3개: 토큰 · 시간 · 발화."""
import json, glob
from datetime import datetime
REC='/Users/kknaks/orca/workspaces/kknaks_profile/아이디어-검토/reference/2026-11-12-interpreter-idea/records/'
FLAT=20000; M=[0.3,0.4,0.5,0.6,0.7]
# 토큰: 실측 2건(1.4) 원/천 토큰
probe={'상담':(53.73,6494+730+515+183+379),'간단':(34.44,5698+128+82+31+51)}
tok={k:c/t*1000 for k,(c,t) in probe.items()}
# 시간: 3절 적정 1시간 원가
hour=json.load(open('sec3.json'))['base']['per_hour']
# 발화: 베타 실사용(운영 기록 11-11~11-14) — 세션 원가 = 연결 42.4 + STT 0.023×연결초 + (0.272+0.047)×추정 음성초(번역 글자 × 0.13초)
S={}
for f in sorted(glob.glob(REC+'*.jsonl')):
    for l in open(f):
        r=json.loads(l); s=S.setdefault(r['session'],{'n':0,'tch':0}); t=datetime.fromisoformat(r['at'])
        if r['type']=='session_start': s['a']=t
        elif r['type']=='session_end': s['b']=t
        else: s['n']+=1; s['tch']+=len(r.get('translation',''))
cost=n=0; sess=0
for s in S.values():
    if 'a' in s and 'b' in s:
        cost+=42.4+0.023*(s['b']-s['a']).total_seconds()+(0.272+0.047)*s['tch']*0.13; n+=s['n']; sess+=1
utt=cost/n
out=dict(tok=tok,hour=hour,utt=utt,beta=dict(sessions=sess,utterances=n,cost=cost),rows=[])
for m in M:
    b=FLAT*(1-m)
    out['rows'].append(dict(m=m,budget=b,tok_lo=b/tok['상담']*1000,tok_hi=b/tok['간단']*1000,hours=b/hour,utts=b/utt))
json.dump(out,open('sec5.json','w'),ensure_ascii=False,indent=1)
print({k:round(v,3) for k,v in tok.items()},round(hour,1),round(utt,2),out['beta'])
for r in out['rows']: print(r['m'],round(r['budget']),round(r['tok_lo']/1e4),round(r['tok_hi']/1e4),round(r['hours'],1),round(r['utts']))
