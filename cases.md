# 十例逐样本核验

固定配置：10k、seed=17；先按 ID 顺序在共同错误、bigram 退化、bigram 纠正、共同正确中各取前两例，再从共同错误补足十例。此选法不代表随机抽样，类别占比以 error_categories.json 为准。

标签：1 World，2 Sports，3 Business，4 Sci/Tech。每例仅引述短片段；完整输入从固定数据源按 ID 恢复。



## test:000004  both_wrong

真值 Sci/Tech；unigram Sports；bigram Sports。

> prediction unit helps forecast wildfires ( ap ) ap - it ' s barely dawn when mike fitzpatrick starts his shift with a blur of colorful maps ,

野火预测属于科技／环境报道，两种模型均判为体育，且置信度约 0.72。它说明高预测分数不保证正确；仅靠局部词组仍可能漏掉整篇报道的主题。尚未做词级归因，不能把错误确定归因于某个词。

逐条证据：[unigram](runs/n10000_g1_s17/test.jsonl) / [bigram](runs/n10000_g2_s17/test.jsonl)，按 id 检索。



## test:000005  both_wrong

真值 Sci/Tech；unigram World；bigram World。

> calif . aims to limit farm-related smog ( ap ) ap - southern california ' s smog-fighting agency went after emissions of the bovine variety friday , adopting

减排规章同时包含环境技术和地方公共治理信息，真值为科技，两种模型均判为世界新闻。这是相邻主题的边界案例；不能仅凭模型分歧认定标注错误。

逐条证据：[unigram](runs/n10000_g1_s17/test.jsonl) / [bigram](runs/n10000_g2_s17/test.jsonl)，按 id 检索。



## test:000009  bigram_regression

真值 Sci/Tech；unigram Sci/Tech；bigram Business。

> e-mail scam targets police chief wiltshire police warns about phishing after its fraud squad chief was targeted .

网络钓鱼报道包含 e-mail 和 phishing，也包含诈骗语境。unigram 判对科技，bigram 判为商业。词组特征并未稳定保留技术线索；具体作用仍需归因实验验证。

逐条证据：[unigram](runs/n10000_g1_s17/test.jsonl) / [bigram](runs/n10000_g2_s17/test.jsonl)，按 id 检索。



## test:000020  bigram_regression

真值 Sci/Tech；unigram Sci/Tech；bigram Business。

> storage , servers bruise hp earnings update earnings per share rise compared with a year ago , but company misses analysts ' expectations by a long shot .

HP 服务器与盈利预期同时出现。真值为科技；unigram 判对，bigram 判商业。商业／科技边界与词组稀疏性都是可能因素，但单条案例无法识别因果。

逐条证据：[unigram](runs/n10000_g1_s17/test.jsonl) / [bigram](runs/n10000_g2_s17/test.jsonl)，按 id 检索。



## test:000021  bigram_fix

真值 Sci/Tech；unigram Business；bigram Sci/Tech。

> ibm to hire even more new workers by the end of the year , the computing giant plans to have its biggest headcount since 1991 .

IBM 招聘报道兼有就业和计算机公司信息。bigram 从商业纠正为科技，说明它在部分样本有效；这不能替代整体准确率与净纠正数。

逐条证据：[unigram](runs/n10000_g1_s17/test.jsonl) / [bigram](runs/n10000_g2_s17/test.jsonl)，按 id 检索。



## test:000105  bigram_fix

真值 World；unigram Sports；bigram World。

> mr downer shoots his mouth off just what alexander downer was thinking when he declared on radio last friday that quot they could fire a missile from north

报道涉及澳大利亚官员与朝鲜导弹言论，真值为世界新闻。bigram 将 unigram 的体育错误纠正；具体局部词组是否起作用仍未检验。

逐条证据：[unigram](runs/n10000_g1_s17/test.jsonl) / [bigram](runs/n10000_g2_s17/test.jsonl)，按 id 检索。



## test:000001  both_correct

真值 Business；unigram Business；bigram Business。

> fears for t n pension after talks unions representing workers at turner newall say they are ' disappointed ' after talks with stricken parent firm federal mogul .

养老金与企业谈判属于商业，两种模型均判对。bigram 分数较低并不等于预测错误；本实验未做概率校准。

逐条证据：[unigram](runs/n10000_g1_s17/test.jsonl) / [bigram](runs/n10000_g2_s17/test.jsonl)，按 id 检索。



## test:000002  both_correct

真值 Sci/Tech；unigram Sci/Tech；bigram Sci/Tech。

> the race is on second private team sets launch date for human spaceflight ( space . com ) space . com - toronto , canada -- a second\team

私人载人航天的主题明确，两种模型均正确判为科技。这是成功对照，说明模型能识别清晰的领域信息。

逐条证据：[unigram](runs/n10000_g1_s17/test.jsonl) / [bigram](runs/n10000_g2_s17/test.jsonl)，按 id 检索。



## test:000010  both_wrong

真值 Sci/Tech；unigram Business；bigram Business。

> card fraud unit nets 36 , 000 cards in its first two years , the uk ' s dedicated card fraud unit , has recovered 36 , 000

银行卡诈骗报道真值为科技，两种模型均判商业；金融词汇与安全技术主题交叉，是需要上下文判别的边界。

逐条证据：[unigram](runs/n10000_g1_s17/test.jsonl) / [bigram](runs/n10000_g2_s17/test.jsonl)，按 id 检索。



## test:000016  both_wrong

真值 Sci/Tech；unigram Business；bigram Business。

> teenage t . rex ' s monster growth tyrannosaurus rex achieved its massive size due to an enormous growth spurt during its adolescent years .

恐龙生长属于科学，两种模型均判为商业。growth 等词可能跨域使用；这只是待检验解释，并非已确认的词级因果证据。

逐条证据：[unigram](runs/n10000_g1_s17/test.jsonl) / [bigram](runs/n10000_g2_s17/test.jsonl)，按 id 检索。