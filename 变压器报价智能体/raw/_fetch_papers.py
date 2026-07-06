#!/usr/bin/env python
"""
Jina fetch key papers for detailed analysis
"""
import sys, os, json, time, subprocess

URLS = [
    # IEEE Review paper on transformer design optimization
    "https://ieeexplore.ieee.org/document/11208581",
    # Space reduction technique for FEA design optimization
    "https://mseee.semnan.ac.ir/article_6885_bc28ca77bd3d3e1b87bab344fd065c1d.pdf",
    # Dual-population for EM large solution space
    "https://pmc.ncbi.nlm.nih.gov/articles/PMC11901470/",
    # Machine learning for EM design optimization
    "https://www.mdpi.com/2076-3417/11/4/1627",
    # Multi-objective optimization for transformer design
    "https://www.mdpi.com/2079-9292/14/6/1198",
]

for url in URLS:
    print(f"\n{'='*60}")
    print(f"FETCHING: {url}")
    print('='*60)
    try:
        result = subprocess.run(
            ["curl", "-sL", f"https://r.jina.ai/{url}"],
            capture_output=True, text=True, timeout=30
        )
        text = result.stdout[:3000]
        print(text)
    except Exception as e:
        print(f"  ERROR: {e}")
    time.sleep(1.5)
