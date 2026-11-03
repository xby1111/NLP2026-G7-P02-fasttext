# G7 分工、贡献与个人核验

论文号：P02。联系人：尚未指定。四位成员信息由本组提供；以下为本次安排的职责，个人完成情况需要对应本人核验记录。现有实验由 Codex 辅助自动运行，暂不将其归为某成员已经独立完成的操作。

| 成员 | 学号 | 分配职责 | 对应成果与个人核验路径 | 当前个人核验状态 |
|---|---|---|---|---|
| 万燊涵 | 1120233197 | 论文理解与整体统稿：定位原文结论，说明方法、复现范围及差异，整合报告与开场讲解 | 核对原文 §2.2、§3.1、表1 AG列；检查 report.pdf 第1、3页；负责 PPT 第1—3页的讲解准备 | 待本人核验并记录 |
| 徐铂尧 | 1120232601 | 数据与固定划分：来源追溯、许可说明、预处理、分层抽样、哈希及重复文本审计 | code/download_data.py、experiment.py 的 prepare；data/README.md、manifest.json、split_ids.csv；核对 train:052295 / test:003304 重叠 | 待本人核验并记录 |
| 唐源锴 | 1120232588 | 环境与实验实现：依赖适配、试跑、参数和种子管理、18次运行、原始日志与计时口径 | requirements.txt、configs/experiment.json、results/environment.json、full_run.log、runs/*/config.json 与 raw.log；负责一分钟运行证据演示准备 | 待本人核验并记录 |
| 齐锴 | 1120231190 | 独立评价与错误分析：Accuracy/Macro-F1、配对差值、规模扩展、十例分析及结果展示 | code/verify_results.py、analyze.py；results/verification.json、summary.csv、paired_deltas.json、cases.md；负责 PPT 第5—7页结果与结论准备 | 待本人核验并记录 |

分工按研究解释、数据、实验、评价四个环节安排。报告与 PPT 由四人共同复核；第4页设置由徐铂尧和唐源锴核对。每人均应能说明整体方法、主要结果、限制及本人负责部分。分配职责不用于推定实际贡献比例，也不表示已经完成个人答问准备。

## 每人需留下的最小证据

- 万燊涵：在 results/personal_verification/1120233197.md 写明原文目标位置、91.5%→92.5%与本组结果的区别，以及一处设置差异。
- 徐铂尧：在 results/personal_verification/1120232601.md 保存数据哈希核对、固定划分数量与互斥/嵌套检查记录。重新 prepare 时使用项目副本，保留原提交证据。
- 唐源锴：在 results/personal_verification/1120232588.md 选一组 uni/bi 对照，核对输入 SHA256相同且仅 wordNgrams 不同，解释日志与计时范围；如重新运行，请用副本保存新日志。
- 齐锴：执行 python code/verify_results.py 后，在 results/personal_verification/1120231190.md 记录本人执行时间和输出，再逐条核对 test:000004、test:000020 的真值与两法预测。

各人记录应包含本人姓名、日期、实际操作/命令、输出位置、发现和能独立解释的结论。目前未收到个人执行证据，故未生成冒充个人日志的记录。本人完成后再将状态更新为“已核验”，并据实修订职责与实际贡献。

## AI 与代码来源

Codex 辅助阅读论文和仓库、编写代码、取得固定公开数据、在本机自动运行18次实验、独立评价与重复性检查，生成中期记录、报告和演示稿。训练与推理由 fastText 实际执行，数值来自日志和逐样本输出；成员分工为后续责任安排，个人操作与理解须由本人证明。

作者代码：https://github.com/facebookresearch/fastText，用户提供 main ZIP；实际引擎 fasttext-wheel==0.9.2。核心训练未修改，适配与评价代码见 code/。数据、许可和固定划分见 data/README.md；版本与哈希见 code/source_provenance.json、results/environment.json。
