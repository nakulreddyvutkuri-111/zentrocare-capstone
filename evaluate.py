"""Diagnostic retrieval evaluation; NOT end-to-end answer accuracy."""
from pathlib import Path
import csv,json,subprocess,sys
from collections import Counter
from src.agent import Retriever,DATA
ROOT=Path(__file__).resolve().parent
R=Retriever(); records=[]
with open(DATA/'practice/questions.csv',encoding='utf-8') as f:
    questions=list(csv.DictReader(f))
for row in questions:
    gold=[s.strip() for s in row['gold_evidence'].split(' ; ') if s.strip() and '.csv:' not in s]
    for variant in ['question','asr_text']:
        hits=R.search(row[variant],5);ids=[h['id'] for h in hits]
        rec={'id':row['id'],'language':row['language'],'variant':variant,'answerable':row['answerable'],'gold':' ; '.join(gold),'retrieved':' ; '.join(ids),'top_score':hits[0]['score'],'gold_count':len(gold)}
        for k in [1,3,5]:rec[f'recall_at_{k}']=sum(g in ids[:k] for g in gold)/len(gold) if gold else ''
        rec['reciprocal_rank']=next((1/(i+1) for i,g in enumerate(ids) if g in gold),0) if gold else ''
        records.append(rec)
with open(ROOT/'reports/retrieval_results.csv','w',newline='',encoding='utf-8') as f:
    w=csv.DictWriter(f,fieldnames=records[0].keys());w.writeheader();w.writerows(records)
summary={}
for variant in ['question','asr_text']:
    valid=[r for r in records if r['variant']==variant and r['gold_count']]
    summary[variant]={'evaluated_questions':len(valid),**{key:round(sum(float(r[key]) for r in valid)/len(valid),4) for key in ['recall_at_1','recall_at_3','recall_at_5','reciprocal_rank']}}
summary['by_language']={}
for lang in sorted(set(r['language'] for r in records)):
    valid=[r for r in records if r['variant']=='question' and r['gold_count'] and r['language']==lang]
    if valid:summary['by_language'][lang]={'n':len(valid),'recall_at_5':round(sum(float(r['recall_at_5']) for r in valid)/len(valid),4)}
summary['indexed_sections']=len(R.chunks)
summary['total_questions']=len(questions)
summary['unanswerable_questions']=sum(r['answerable']=='False' for r in questions)
(ROOT/'reports/metrics.json').write_text(json.dumps(summary,indent=2))
print(json.dumps(summary,indent=2))
