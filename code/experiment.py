"""AG News fastText controlled reproduction. Run from the package root."""
import argparse, collections, csv, datetime, gc, hashlib, importlib.metadata
import json, os, pathlib, platform, random, re, statistics, subprocess, sys, time

ROOT = pathlib.Path(__file__).resolve().parents[1]
def dump(path, obj):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(obj, ensure_ascii=False, indent=2), encoding='utf-8')
def sha(path): return hashlib.sha256(path.read_bytes()).hexdigest()
def norm(s):
    # Explicit deterministic adaptation of the author's sed/tr pipeline.
    s = s.lower().replace('<br />', ' ').replace('"', '')
    s = re.sub(r"([\'.,()!?])", r' \1 ', s)
    s = s.replace(';', ' ').replace(':', ' ')
    return ' '.join(s.split())
def read_csv(path, prefix):
    out=[]
    with path.open(encoding='utf-8', newline='') as f:
        for i,row in enumerate(csv.reader(f),1):
            assert len(row)==3 and row[0] in ('1','2','3','4'), (i,row)
            out.append(dict(id=f'{prefix}:{i:06d}', label=int(row[0]), text=norm(row[1]+' '+row[2])))
    return out
def metrics(gold,pred):
    assert len(gold)==len(pred) and len(gold)>0
    cm=[[sum(y==i and p==j for y,p in zip(gold,pred)) for j in range(1,5)] for i in range(1,5)]
    f1=[]
    for i in range(4):
        tp=cm[i][i]; fp=sum(cm[j][i] for j in range(4))-tp; fn=sum(cm[i])-tp
        f1.append(2*tp/(2*tp+fp+fn) if 2*tp+fp+fn else 0)
    return dict(accuracy=sum(y==p for y,p in zip(gold,pred))/len(gold), macro_f1=sum(f1)/4, confusion=cm, per_class_f1=f1, n=len(gold))
def prepare(raw, work):
    cfg=json.loads((ROOT/'configs/experiment.json').read_text(encoding='utf-8'))
    train=read_csv(raw/'train.csv','train'); test=read_csv(raw/'test.csv','test')
    assert len(train)==120000 and len(test)==7600
    rng=random.Random(cfg['split_seed']); pools={c:[x for x in train if x['label']==c] for c in range(1,5)}
    val=[]; chosen={n:[] for n in cfg['sizes']}
    for c,rows in pools.items():
        rng.shuffle(rows); val+=rows[:cfg['validation_size']//4]; pool=rows[cfg['validation_size']//4:]
        for n in chosen: chosen[n]+=pool[:n//4]
    val.sort(key=lambda x:x['id']); test.sort(key=lambda x:x['id'])
    work.mkdir(parents=True,exist_ok=True)
    for name,rows in [('validation',val),('test',test)]+[(f'train_{n}',v) for n,v in chosen.items()]:
        with (work/(name+'.jsonl')).open('w',encoding='utf-8') as f:
            for x in rows:f.write(json.dumps(x,ensure_ascii=False)+'\n')
    ids=[]
    for name,rows in [('validation',val),('test',test)]+[(f'train_{n}',v) for n,v in chosen.items()]:
        ids += [dict(split=name,id=x['id'],label=x['label']) for x in rows]
    with (ROOT/'data/split_ids.csv').open('w',encoding='utf-8',newline='') as f:
        w=csv.DictWriter(f,fieldnames=['split','id','label']);w.writeheader();w.writerows(ids)
    for n,rows in chosen.items():
        assert not set(x['id'] for x in rows)&set(x['id'] for x in val)
        for seed in cfg['seeds']:
            ordered=rows.copy();random.Random(seed).shuffle(ordered)
            (work/f'train_{n}_s{seed}.txt').write_text(''.join(f"__label__{x['label']} {x['text']}\n" for x in ordered),encoding='utf-8')
    hashes={n:dict(csv_sha256=sha(raw/(n+'.csv'))) for n in ('train','test')}
    hashes['audit']={}
    ts=set(x['text'] for x in test);vs=set(x['text'] for x in val)
    for n,rows in chosen.items():
        texts=[x['text'] for x in rows]
        hashes['audit'][str(n)]={'unique_texts':len(set(texts)), 'train_validation_text_overlap':len(set(texts)&vs),'train_test_text_overlap':len(set(texts)&ts)}
    hashes['split_ids_sha256']=sha(ROOT/'data/split_ids.csv')
    hashes['normalized_jsonl_sha256']={p.name:sha(p) for p in work.glob('*.jsonl')}
    hashes['created_at']=datetime.datetime.now(datetime.timezone(datetime.timedelta(hours=8))).isoformat()
    dump(ROOT/'data/manifest.json',hashes)
    print('PREPARED',hashes,flush=True)
def load_rows(work,name):return [json.loads(x) for x in (work/(name+'.jsonl')).read_text(encoding='utf-8').splitlines()]
def worker(work,n,ng,seed,smoke=False):
    import fasttext
    cfg=json.loads((ROOT/'configs/experiment.json').read_text(encoding='utf-8'))
    run=f'n{n}_g{ng}_s{seed}'+('_smoke' if smoke else '')
    out=ROOT/'results'/('smoke' if smoke else 'runs')/run;out.mkdir(parents=True,exist_ok=True)
    params=cfg['fasttext'].copy();params.update(wordNgrams=ng,seed=seed)
    file=work/f'train_{n}_s{seed}.txt'
    if smoke:
        p=work/'smoke.txt';p.write_text('\n'.join(file.read_text(encoding='utf-8').splitlines()[:100])+'\n',encoding='utf-8');file=p
        params['epoch']=1
    dump(out/'config.json',{'run_id':run,'n_train':100 if smoke else n,'input_sha256':sha(file),'params':params,'started_at':datetime.datetime.now(datetime.timezone.utc).isoformat()})
    start=time.perf_counter();model=fasttext.train_supervised(input=str(file),**params);train_s=time.perf_counter()-start
    result={'run_id':run,'size':n,'ngram':ng,'seed':seed,'train_seconds':train_s,'vocabulary_size':len(model.words),'params':params}
    for split in ['validation','test']:
        rows=load_rows(work,split)
        if smoke:rows=rows[:32]
        texts=[x['text'] for x in rows]
        model.predict(texts[:min(32,len(texts))])  # excluded warm-up
        elapsed=[]
        for _ in range(3):
            start=time.perf_counter();labels,probs=model.predict(texts,k=1);elapsed.append(time.perf_counter()-start)
        pred=[int(x[0].replace('__label__','')) for x in labels]
        m=metrics([x['label'] for x in rows],pred);m['inference_seconds']=statistics.median(elapsed);m['inference_repeats_seconds']=elapsed
        result[split]=m
        with (out/(split+'.jsonl')).open('w',encoding='utf-8') as f:
            for x,y,p in zip(rows,pred,probs):
                f.write(json.dumps({'id':x['id'],'gold':x['label'],'pred':y,'confidence':float(p[0]),'run_id':run,'config':'config.json'},ensure_ascii=False)+'\n')
    dump(out/'metrics.json',result)
    print(json.dumps(result),flush=True)
def summarize():
    rows=[json.loads(p.read_text(encoding='utf-8')) for p in sorted((ROOT/'results/runs').glob('*/metrics.json'))]
    cfg=json.loads((ROOT/'configs/experiment.json').read_text(encoding='utf-8'))
    assert len(rows)==len(cfg['sizes'])*2*len(cfg['seeds'])
    flat=[]
    for r in rows:
        flat.append({k:r[k] for k in ['run_id','size','ngram','seed','train_seconds','vocabulary_size']}|{f'{s}_{k}':r[s][k] for s in ['validation','test'] for k in ['accuracy','macro_f1','inference_seconds']})
    with (ROOT/'results/all_runs.csv').open('w',encoding='utf-8',newline='') as f:
        w=csv.DictWriter(f,fieldnames=list(flat[0]));w.writeheader();w.writerows(flat)
    agg=[]
    for n in cfg['sizes']:
        for g in [1,2]:
            rr=[r for r in flat if r['size']==n and r['ngram']==g];o={'size':n,'ngram':g,'runs':len(rr)}
            for k in ['test_accuracy','test_macro_f1','train_seconds','test_inference_seconds','validation_accuracy']:
                o[k+'_mean']=statistics.mean(x[k] for x in rr);o[k+'_sd']=statistics.stdev(x[k] for x in rr)
            agg.append(o)
    dump(ROOT/'results/summary.json',agg)
    with (ROOT/'results/summary.csv').open('w',encoding='utf-8',newline='') as f:
        w=csv.DictWriter(f,fieldnames=list(agg[0]));w.writeheader();w.writerows(agg)
    delta=[]
    for n in cfg['sizes']:
        ds=[]
        for s in cfg['seeds']:
            pair={r['ngram']:r for r in flat if r['size']==n and r['seed']==s}
            ds.append((pair[2]['test_accuracy']-pair[1]['test_accuracy'])*100)
        delta.append({'size':n,'paired_accuracy_delta_pp':ds,'mean_pp':statistics.mean(ds),'sd_pp':statistics.stdev(ds)})
    dump(ROOT/'results/paired_deltas.json',delta)
    print('SUMMARY',json.dumps(agg),flush=True)
def main():
    p=argparse.ArgumentParser();p.add_argument('action',choices=['prepare','run','worker','summarize']);p.add_argument('--raw',type=pathlib.Path,default=ROOT/'data/raw');p.add_argument('--work',type=pathlib.Path,default=ROOT/'data/prepared');p.add_argument('--size',type=int,default=1000);p.add_argument('--ngram',type=int,default=1);p.add_argument('--seed',type=int,default=17);p.add_argument('--smoke',action='store_true');a=p.parse_args()
    if a.action=='prepare':prepare(a.raw,a.work)
    elif a.action=='worker':worker(a.work,a.size,a.ngram,a.seed,a.smoke)
    elif a.action=='summarize':summarize()
    else:
        cfg=json.loads((ROOT/'configs/experiment.json').read_text(encoding='utf-8'))
        for n in cfg['sizes']:
            for s in cfg['seeds']:
                for g in ([1,2] if s%2 else [2,1]):
                    out=ROOT/f'results/runs/n{n}_g{g}_s{s}';out.mkdir(parents=True,exist_ok=True)
                    with (out/'raw.log').open('w',encoding='utf-8') as f:
                        cmd=[sys.executable,str(pathlib.Path(__file__).resolve()),'worker','--work',str(a.work.resolve()),'--size',str(n),'--ngram',str(g),'--seed',str(s)]
                        f.write('COMMAND '+json.dumps(cmd)+'\n');f.flush();subprocess.run(cmd,stdout=f,stderr=subprocess.STDOUT,check=True)
                    print('DONE',out.name,flush=True)
        summarize()
if __name__=='__main__':main()
