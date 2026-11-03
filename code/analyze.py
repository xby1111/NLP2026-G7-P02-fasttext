"""Overlap sensitivity, deterministic case selection, and evidence indexes."""
import argparse,collections,csv,json,pathlib,statistics,sys
from experiment import ROOT,load_rows,metrics,dump

def main():
    p=argparse.ArgumentParser();p.add_argument('--work',type=pathlib.Path,default=ROOT/'data/prepared');a=p.parse_args()
    test=load_rows(a.work,'test');validation=load_rows(a.work,'validation');train=load_rows(a.work,'train_10000')
    train_text={x['text'] for x in train}
    excluded={x['id'] for x in test if x['text'] in train_text}
    overlap=[{'test_id':x['id'],'train_ids':[t['id'] for t in train if t['text']==x['text']]} for x in test if x['id'] in excluded]
    sensitivity=[]
    for path in sorted((ROOT/'results/runs').glob('*/metrics.json')):
        m=json.loads(path.read_text(encoding='utf-8'))
        rr=[json.loads(x) for x in (path.parent/'test.jsonl').read_text(encoding='utf-8').splitlines()]
        clean=[x for x in rr if x['id'] not in excluded]
        sensitivity.append({k:m[k] for k in ['run_id','size','ngram','seed']}|metrics([x['gold'] for x in clean],[x['pred'] for x in clean]))
    dump(ROOT/'results/overlap_sensitivity.json',{'policy':'Remove the union of normalized test texts also present in the fixed 10k training subset; use this SAME reduced test set for all 18 runs. Main metrics retain the official 7600-example test set.','excluded':overlap,'clean_test_n':len(test)-len(excluded),'runs':sensitivity})
    preds={}
    for ng in [1,2]:
        preds[ng]={x['id']:x for x in [json.loads(line) for line in (ROOT/f'results/runs/n10000_g{ng}_s17/test.jsonl').read_text(encoding='utf-8').splitlines()]}
    groups=collections.defaultdict(list)
    for x in test:
        u=preds[1][x['id']];b=preds[2][x['id']]
        key=('both_correct' if u['pred']==x['label'] and b['pred']==x['label'] else 'bigram_fix' if b['pred']==x['label'] else 'bigram_regression' if u['pred']==x['label'] else 'both_wrong')
        groups[key].append(x)
    chosen=[]
    for key in ['both_wrong','bigram_regression','bigram_fix','both_correct']:
        # First ID within each category, two per group; then fill to ten with both-wrong.
        for x in groups[key][:2]:chosen.append((key,x))
    seen={x['id'] for _,x in chosen}
    for x in groups['both_wrong']:
        if len(chosen)>=10:break
        if x['id'] not in seen:chosen.append(('both_wrong',x));seen.add(x['id'])
    cases=[]
    for key,x in chosen:
        u=preds[1][x['id']];b=preds[2][x['id']]
        cases.append({'id':x['id'],'category':key,'gold':x['label'],'unigram_pred':u['pred'],'bigram_pred':b['pred'],'unigram_confidence':u['confidence'],'bigram_confidence':b['confidence'],'excerpt':' '.join(x['text'].split()[:28]),'source_note':'Short quotation for error analysis. Recover complete text from the fixed public source and sample ID.','analysis':'待结合原文语义解释'})
    dump(ROOT/'results/cases.json',cases)
    dump(ROOT/'results/error_categories.json',{k:len(v) for k,v in groups.items()})
    print(json.dumps({'excluded':overlap,'groups':{k:len(v) for k,v in groups.items()},'cases':cases},ensure_ascii=False,indent=2))
if __name__=='__main__':main()
