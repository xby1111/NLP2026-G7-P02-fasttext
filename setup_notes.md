# 环境与资源排查记录

实际日期 2026-11-03。读取用户论文与源码 ZIP；原始附件未改动。

1. 本机无已安装 fasttext，未发现可直接调用的 C++ 编译器。固定 fasttext-wheel 0.9.2 的 cp311 win_amd64 wheel，解压到隔离的运行目录后使用，未修改全局 Python 包。
2. 早期 Windows curl HTTPS 报错：schannel: AcquireCredentialsHandle failed: SEC_E_NO_CREDENTIALS (0x8009030E)。Python 公共数据请求也发生读入不完整：IncompleteRead(425984 bytes read)。这些是下载错误，不是训练错误。
3. 之后通过 Python HTTPS 固定 GitHub commit，分段读取 train.csv，按 Git blob ID 校验后组装，最终 SHA256 见 data/manifest.json。测试 CSV 也核验对应 blob/哈希。
4. 100 条真实 AG News、1 epoch 试跑成功，再启动 18 次正式运行；每次独立进程，CPU 单线程；没有使用生成服务。
5. 完整验证与测试预测用 scikit-learn 独立核对；10k bigram seed=17 重新训练后全部标签及分数一致。审计检查出单条测试文本重叠，另做共同评价子集的敏感性分析。

本说明据当前会话实际错误与成功操作整理，不是历史中期进度的倒填。原始正式训练日志在 runs/*/raw.log；网络排查不是模型效果证据。
