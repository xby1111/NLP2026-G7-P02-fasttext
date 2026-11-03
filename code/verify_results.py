"""Independent metric and sample-ID verification with scikit-learn."""
import csv, json, pathlib, statistics
from sklearn.metrics import accuracy_score, f1_score, confusion_matrix
ROOT=pathlib.Path(__file__).resolve().parents[1]
def main():
    splits={}
    with (ROOT/'data/split_ids.csv').open(encoding='utf-8') as f:
        for row in csv.DictReader(f):splits.setdefault(row['split'],{})[row['id']]=int(row['label'])
    cfg=json.loads((ROOT/'configs/experiment.json').read_text(encoding='utf-8'))
    files=sorted((ROOT/'results/runs').glob('*/metrics.json'))
    assert len(files)==18
    checked=0
    for path in files:
        m=json.loads(path.read_text(encoding='utf-8'))
        for split in ['test','validation']:
            rows=[json.loads(line) for line in (path.parent/(split+'.jsonl')).read_text(encoding='utf-8').splitlines()]
            assert len({r['id'] for r in rows})==len(rows)==len(splits[split])
            assert {r['id'] for r in rows}==set(splits[split])
            assert all(r['gold']==splits[split][r['id']] and r['run_id']==m['run_id'] for r in rows)
            gold=[r['gold'] for r in rows];pred=[r['pred'] for r in rows]
            assert abs(accuracy_score(gold,pred)-m[split]['accuracy'])<1e-12
            assert abs(f1_score(gold,pred,labels=[1,2,3,4],average='macro')-m[split]['macro_f1'])<1e-12
            assert confusion_matrix(gold,pred,labels=[1,2,3,4]).tolist()==m[split]['confusion']
            checked+=len(rows)
    for n in cfg['sizes']:
        assert len(splits[f'train_{n}'])==n
        assert not set(splits[f'train_{n}'])&set(splits['validation'])
    assert set(splits['train_1000'])<=set(splits['train_5000'])<=set(splits['train_10000'])
    result={'status':'PASS','runs':18,'predictions_checked':checked,'independent_metrics':'scikit-learn accuracy_score, f1_score, confusion_matrix','nested_subsets':True,'train_validation_id_disjoint':True}
    (ROOT/'results/verification.json').write_text(json.dumps(result,indent=2),encoding='utf-8')
    print(json.dumps(result,indent=2))
if __name__=='__main__':main()
