"""
引擎效率提升方案 联网搜索
搜索关键词组：
1. 变压器优化计算 引擎 效率 提升 剪枝 并行
2. transformer design optimization nested loop pruning memoization
3. 电机变压器计算 加速技术 缓存 并行计算
4. transformer electromagnetic calculation optimization techniques
5. java大型工程计算 优化 性能 改造经验
"""
import sys, os, json, time

sys.path.insert(0, r'D:\hermes\skills\thingcom-tech-research\scripts')
from ddgs_search import search

queries = [
    "变压器优化计算 引擎 效率 剪枝 并行计算",
    "transformer design optimization nested loop pruning caching",
    "电磁计算 搜索空间 减少 加速技术 缓存",
    "electromagnetic design optimization search space reduction techniques",
    "java 工程计算 性能优化 循环剪枝 并行 缓存",
    "电机设计 优化计算 加速 解耦 分步优化",
    "finite element analysis nested loop optimization memoization pattern",
    "engineering optimization calculation engine speedup techniques comparison"
]

results = {}
for q in queries:
    print(f"\n=== 搜索: {q} ===")
    try:
        res = search(q, max_results=8, timeout=30)
        results[q] = res
        print(json.dumps(res, ensure_ascii=False, indent=2)[:2000])
    except Exception as e:
        print(f"搜索失败: {e}")
    time.sleep(1)

# 汇总输出
print("\n\n========== 搜索结果汇总 ==========")
for q, res in results.items():
    print(f"\n--- {q[:30]}... ---")
    if isinstance(res, list):
        for r in res[:5]:
            print(f"  [{r.get('source','?')}] {r.get('title','?')[:60]}")
            print(f"    {r.get('href','?')}")
    else:
        print(f"  结果类型: {type(res)}")

print("\n搜索完成")
