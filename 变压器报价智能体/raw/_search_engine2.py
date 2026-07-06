#!/usr/bin/env python
"""
独立搜索脚本：引擎效率提升方案相关关键词
直接调用 ddgs 库搜索，不依赖外部模块。
"""
import sys, json, time

# 确保 ddgs 路径
sys.path.insert(0, r'C:\Users\keming\AppData\Roaming\Python\Python314\site-packages')

from ddgs import DDGS

QUERIES = [
    "变压器优化计算 引擎 效率 剪枝 并行计算",
    "transformer design optimization nested loop pruning caching",
    "电磁计算 搜索空间 减少 加速技术 缓存",
    "electromagnetic design optimization search space reduction",
    "Java 工程计算 性能优化 循环剪枝 并行计算",
    "电机设计 优化计算 加速 解耦 分步优化",
    "design optimization nested loop speedup memoization",
    "engineering calculation engine optimization techniques comparison"
]

def search(query: str, max_results: int = 8):
    d = DDGS()
    results = []
    try:
        for r in d.text(query, max_results=max_results):
            results.append({
                "href": r.get("href", ""),
                "title": r.get("title", ""),
                "body": r.get("body", "")[:300]
            })
    except Exception as e:
        print(f"  ERROR: {e}", file=sys.stderr)
    return results

all_results = {}
for q in QUERIES:
    print(f"\n{'='*60}")
    print(f"QUERY: {q}")
    print('='*60)
    res = search(q, max_results=8)
    all_results[q] = res
    if not res:
        print("  (no results)")
    else:
        for r in res:
            print(f"  URL: {r['href']}")
            print(f"  TITLE: {r['title'][:80]}")
            print(f"  SNIPPET: {r['body'][:200]}")
            print()
    time.sleep(1.5)

# 输出汇总 JSON
summary = json.dumps(all_results, ensure_ascii=False, indent=2)
print("\n\n========== JSON SUMMARY ==========")
print(summary[:5000])
