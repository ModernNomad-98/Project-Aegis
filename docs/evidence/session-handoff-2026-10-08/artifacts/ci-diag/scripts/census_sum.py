import json, sys, collections
rows = [json.loads(l) for l in open(sys.argv[1])]
print("fixtures censused:", len(rows))
by = collections.defaultdict(list)
for r in rows: by[r["test"]].append(r)
for t, v in by.items():
    print(f"{t}: fixtures={len(v)} max_noncommit_in_17={max(x['noncommit_in_17'] for x in v)} commits/fixture={sorted(set(x['commits'] for x in v))}")
def p(d): return 1.0 if d >= 2 else ((1 - (255/256)**2) if d == 1 else (1/256)**2)
tot = sum(p(r["noncommit_in_17"]) for r in rows)
print("expected natural repack triggers per test-file run: %.3g (= 1 per %.0f runs)" % (tot, 1/tot))
