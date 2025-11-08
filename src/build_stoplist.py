#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import argparse
import re
import glob
import os
from collections import Counter

TOKEN_REGEX = re.compile(r"[a-zA-Z]+")

def tokenize(text: str):
    return TOKEN_REGEX.findall(text.lower())

def build_counter(input_dir: str) -> Counter:
    paths = sorted(glob.glob(os.path.join(input_dir, "*.txt")))
    if len(paths) < 10:
        print(f"[אזהרה] נמצאו {len(paths)} קבצים בלבד. ודאי שיש 10 קבצים בתיקייה {input_dir}.")
    counter = Counter()
    for p in paths:
        with open(p, "r", encoding="utf-8", errors="ignore") as f:
            counter.update(tokenize(f.read()))
    return counter

def top_k(counter: Counter, k: int):
    items = list(counter.items())
    items.sort(key=lambda x: (-x[1], x[0]))
    return items[:k]

def main():
    ap = argparse.ArgumentParser(description="Build a top-K stop-list from plain text files.")
    ap.add_argument("--input_dir", required=True, help="תיקייה עם קבצי .txt (למשל data/wiki)")
    ap.add_argument("--k", type=int, default=50, help="כמה מילים נפוצות להחזיר (בררת מחדל: 50)")
    ap.add_argument("--out", required=True, help="נתיב לקובץ פלט topK (למשל out/top50.txt)")
    args = ap.parse_args()

    os.makedirs(os.path.dirname(args.out), exist_ok=True)

    counter = build_counter(args.input_dir)
    topk = top_k(counter, args.k)

    with open(args.out, "w", encoding="utf-8") as f:
        for w, c in topk:
            f.write(f"{w}\t{c}\n")

    print(f"נשמר: {args.out}\n")
    print("Top words:")
    for w, c in topk:
        print(f"{w}\t{c}")

if __name__ == "__main__":
    main()
