# 汇报讲稿与证据演示

前7页主讲总计300秒，第8页证据60秒。现场不重新训练。

## 第1页  25秒

我们复现的是词袋与词组特征的受控比较，范围限定为 AG News。采用三个数据规模和三个种子，共完成18次正式运行。本组为G7，成员与学号已列在首页；联系人尚未指定。

来源：https://aclanthology.org/E17-2068/；results/summary.csv

## 第2页  40秒

目标是第428页的n-gram方法和第429页表1的AG列。原文91.5到92.5是全量实验数值，不是我们的运行成绩。本次保留表示方式，缩小训练集，检查提升是否仍成立。

来源：论文 §2.2、§3.1、表1 AG列；https://aclanthology.org/E17-2068/

## 第3页  45秒

模型把词和词组向量平均，再经线性输出层分类。unigram是同一模型的比较起点，bigram增加相邻词对。不是字符子词，也没有预训练向量。四分类使用softmax，因此这次不检验层级softmax在超大标签空间的速度优势。

来源：论文第427页图1、第428页§2.2；code/experiment.py；configs/experiment.json

## 第4页  45秒

先分层固定4000条验证，再在其余训练记录中构造嵌套子集。同种子两方法的输入文件完全相同。学习率按作者AG脚本预先固定为0.25，验证集没有用来挑最优模型。单线程有利于复查，不能与原文多线程时间直接相比。

来源：data/README.md、split_ids.csv；results/environment.json；code/third_party/fasttext_classification-results.sh

## 第5页  60秒

这张表全部来自真实运行。1k精度较低，不能把训练不足假设说成已证实。5k下bigram劣势明显，10k下接近但仍略低。训练时间包含引擎调用内初始化；推理先预热，再对7600条运行三遍取中位数。方差是三个种子的样本标准差，不是置信区间。

来源：results/summary.csv、all_runs.csv、paired_deltas.json；results/runs/*/raw.log

## 第6页  55秒

更多训练数据改善两种模型，bigram在5k到10k的增益更大，但这不能分离覆盖率、参数量与优化等机制。第一条野火报道两者均错；第二条同时有服务器和盈利语境，bigram发生退化。我们没有做词级归因，语义解释只是可检验假设。

来源：results/cases.md；results/runs/n10000_g1_s17/test.jsonl；results/runs/n10000_g2_s17/test.jsonl

## 第7页  30秒

结论限定为本数据划分和固定参数，不否定原文全量结果。贡献是可追溯的对照、规模扩展和错误分析，而不是获得正提升。AI辅助编写和运行已披露，成员应分别完成自己的核验，贡献表不能虚构。

来源：report.pdf；contributions.md；results/verification.json

## 第8页  60秒

打开入口和配置约10秒；展示summary和metrics约15秒；在bigram逐条文件搜索test:000020，再对照unigram输出约20秒；最后展示208800条独立指标核验通过及7600条重复训练完全一致约15秒。主结果保留官方测试，另对重复文本统一剔除后7599条重算，方向不变。

来源：results/verification.json；reproducibility.json；overlap_sensitivity.json

## 答问准备

1. 为什么没有提升？本设置训练量、学习率搜索和平台与原文不同；机制解释尚未隔离。
2. 为什么算单因素？同规模同种子两法只改wordNgrams；规模扩展另固定方法比较训练量。
3. 如何核验数字？固定样本ID→config→逐样本输出→独立指标→汇总。
4. 三个种子说明什么？当前固定抽样上的训练波动，不能代表抽样间波动。
5. 四个人分别做什么？必须据实填写并能解释各自核验，AI自动运行不等于个人已核验。
