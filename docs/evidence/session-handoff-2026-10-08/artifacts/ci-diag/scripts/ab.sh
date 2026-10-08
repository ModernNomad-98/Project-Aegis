#!/bin/bash
# usage: ab.sh <tree: base|patched> <iterations> <force: 0|1>
S=/tmp/claude-0/-home-user-Project-Aegis/0168d1d5-9af4-5a74-a8dd-9a35339e53ab/scratchpad/ci-diag
G=/tmp/claude-0/-home-user-Project-Aegis/0168d1d5-9af4-5a74-a8dd-9a35339e53ab/scratchpad/git-build/install/bin
tree=$1; n=$2; force=$3; out=$S/repro/ab-$tree-force$force; rm -rf $out; mkdir -p $out/tmp
export PATH=$G:$PATH TMPDIR=$out/tmp GIT_CONFIG_GLOBAL=/dev/null PYTHONDONTWRITEBYTECODE=1
if [ "$force" = 1 ]; then export GIT_CONFIG_COUNT=1 GIT_CONFIG_KEY_0=maintenance.geometric-repack.auto GIT_CONFIG_VALUE_0=-1; fi
cd $S/fixcheck/$tree
pass=0; fail=0; e39=0
for i in $(seq 1 $n); do
  python3 -B -P scripts/tests/test_offline_ci.py ProtectedFileGuardTests > $out/run$i.log 2>&1 && pass=$((pass+1)) || fail=$((fail+1))
  e39=$((e39 + $(grep -c 'Errno 39' $out/run$i.log)))
done
echo "$tree force=$force git=$(git --version | cut -d' ' -f3) runs=$n pass=$pass fail=$fail errno39_errors=$e39 last=$(grep -E '^(OK|FAILED)' $out/run$n.log)"
