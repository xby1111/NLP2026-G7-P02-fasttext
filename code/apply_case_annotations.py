"""Restore the reviewed, fixed-ID case explanations after analyze.py."""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

def main():
    cases_path = ROOT / 'results/cases.json'
    cases = json.loads(cases_path.read_text(encoding='utf-8'))
    annotations = json.loads((ROOT / 'code/case_annotations.json').read_text(encoding='utf-8'))
    labels = {1: 'World', 2: 'Sports', 3: 'Business', 4: 'Sci/Tech'}
    missing = [c['id'] for c in cases if c['id'] not in annotations]
    if missing:
        raise ValueError(f'Unreviewed case IDs: {missing}')
    lines = ['# 十例逐样本核验',
             '固定配置：10k、seed=17；按 ID 顺序在共同错误、bigram 退化、bigram 纠正、共同正确中各取前两例，再从共同错误补足十例。此选法不代表随机抽样，类别占比见 error_categories.json。',
             '标签：1 World，2 Sports，3 Business，4 Sci/Tech。短片段用于分析；完整输入从固定数据源按 ID 恢复。']
    for case in cases:
        case['analysis'] = annotations[case['id']]
        lines.extend([f"## {case['id']}  {case['category']}",
                      f"真值 {labels[case['gold']]}；unigram {labels[case['unigram_pred']]}；bigram {labels[case['bigram_pred']]}。",
                      '> ' + case['excerpt'], case['analysis'],
                      '逐条证据：[unigram](runs/n10000_g1_s17/test.jsonl) / [bigram](runs/n10000_g2_s17/test.jsonl)，按 id 检索。'])
    cases_path.write_text(json.dumps(cases, ensure_ascii=False, indent=2), encoding='utf-8')
    (ROOT / 'results/cases.md').write_text('\n\n'.join(lines), encoding='utf-8')
    print(f'Restored {len(cases)} reviewed cases')

if __name__ == '__main__':
    main()
