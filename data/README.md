# AG News 数据与固定划分

来源论文：https://arxiv.org/abs/1509.01626
数据发布方介绍：http://www.di.unipi.it/~gulli/AG_corpus_of_news_articles.html
可追溯镜像：https://github.com/mhjabreel/CharCnn_Keras/tree/555590db4219b1243abb1918effd6a7425a2d75f/data/ag_news_csv
获取日期：2026-11-03。CSV 无表头，列为 label、title、description；训练 120000，测试 7600。

固定版本 commit：555590db4219b1243abb1918effd6a7425a2d75f。
train.csv SHA256：76a0a2d2f92b286371fe4d4044640910a04a803fdd2538e0f3f29a5c6f6b672e
test.csv SHA256：521465c2428ed7f02f8d6db6ffdd4b5447c1c701962353eb2c40d548c3c85699
Git blob ID：train=694aa19971315410e000404523796b76349d3c1d；test=130b40c3329c993468b8ed8a22c331315e478e0a。

许可：AG 原始新闻文本有新闻发布者权利，公开可下载不等于全部文本可自由再分发。源 CSV 不在提交 ZIP 中。只附样本 ID、标签、模型输出，以及错误分析所必需的少量短引文。上游代码仓库许可不能替代新闻数据许可；请遵守发布方的学术使用及其他限制。

恢复方法（在提交包根目录）：
```powershell
python code/download_data.py --output data/raw --workers 8
python code/experiment.py prepare --raw data/raw --work data/prepared
```

划分：Python 3.11 random.Random(2026)，标签 1→4 依次打乱；每类前 1000 条为验证，之后每类前 250/1250/2500 条为嵌套训练。seed=17/42/2026 只改变训练顺序与初始化。ID 形如 train:000001，指原 CSV 的 1 起始记录序号。固定 ID 在 split_ids.csv（含子集成员重复出现的多行），规范化输出哈希在 manifest.json。重新 prepare 后 ID 和规范化文件哈希应一致，created_at 会变化。

标签：1 World，2 Sports，3 Business，4 Sci/Tech。所有比较用同一 4000 条验证和 7600 条测试；不从测试集调参。输入为标题与描述相连；规范化步骤详见 experiment.py 的 norm。

审计：10k 内部有一条重复文本；5k/10k 与测试各有 1 种重复文本，train:052295→test:003304。保留官方主结果，并在 results/overlap_sensitivity.json 对所有 18 次运行统一排除该测试样本，使用同一 7599 条测试集。没有训练/验证 ID 或完全相同规范化文本交叉。
