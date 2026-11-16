"""price.md 4절 — 요금제 3종 × 마진 30·50·70%. 원가는 1.5 · 3절 값."""
import json
M=[0.3,0.5,0.7]; FLAT=20000; DAYS=30
F=42.4+0.023*60                                   # 연결 1회 고정(연결비 + 무발화 60초)
UNIT={'상담':16.12+F,'간단':2.74+F}               # 대화 1건 = 연결 1회 + 1발화
s3=json.load(open('sec3.json'))
base=s3['base']; ph=base['per_hour']; mc=base['cost']; hours=base['hours']
ph_all={k:[p['per_hour'] for p in v['points'] if p['per_hour']>0] for k,v in s3['sweeps'].items()}
lo=min(min(v) for v in ph_all.values()); hi=max(max(v) for v in ph_all.values())
out={'F':F,'UNIT':UNIT,'per_hour':ph,'month_cost':mc,'ph_lo':lo,'ph_hi':hi,'m':{}}
for m in M:
    r={}
    r['시간제_p']=ph/(1-m); r['시간제_월']=r['시간제_p']*hours
    r['시간제_최악마진']=(r['시간제_p']-hi)/r['시간제_p']
    r['토큰제_배수']=1/(1-m); r['토큰제_월']=mc/(1-m)
    r['토큰제_상담건']=UNIT['상담']/(1-m); r['토큰제_간단건']=UNIT['간단']/(1-m)
    budget=FLAT*(1-m)
    for t in UNIT:
        r[f'정액_{t}_월']=budget/UNIT[t]; r[f'정액_{t}_일']=budget/UNIT[t]/DAYS
        r[f'정액_{t}_초과']=UNIT[t]/(1-m)
    for name,c in [('절반',21.2),('1/4',10.6)]:
        Fc=c+0.023*60
        r[f'정액_상담_일_{name}']=budget/(16.12+Fc)/DAYS; r[f'정액_간단_일_{name}']=budget/(2.74+Fc)/DAYS
    r['정액_적정마진']=(FLAT-mc)/FLAT
    out['m'][m]=r
json.dump(out,open('sec4.json','w'),ensure_ascii=False,indent=1)
f=lambda v:f'{v:,.1f}'
print('F',F,'unit',UNIT,'ph',ph,'mc',mc,'lo',lo,'hi',hi)
for m,r in out['m'].items(): print(m,{k:f(v) for k,v in r.items()})
