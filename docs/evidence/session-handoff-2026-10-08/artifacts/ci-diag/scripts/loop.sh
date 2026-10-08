#!/bin/bash
# usage: loop.sh <label> <iterations> [git-bin-dir]
# Runs scripts/tests/test_offline_ci.py repeatedly from the repo root with a
# scratch TMPDIR and an empty global git config; records one line per run.
label=$1; n=$2; gitdir=$3
S=/tmp/claude-0/-home-user-Project-Aegis/0168d1d5-9af4-5a74-a8dd-9a35339e53ab/scratchpad/ci-diag
out=$S/repro/$label; mkdir -p $out/tmp
[ -n "$gitdir" ] && export PATH=$gitdir:$PATH
export TMPDIR=$out/tmp GIT_CONFIG_GLOBAL=/dev/null PYTHONDONTWRITEBYTECODE=1
cd /home/user/Project-Aegis
echo "git=$(git --version) python=$(python3 --version)" > $out/summary.txt
for i in $(seq 1 $n); do
  python3 -B -P scripts/tests/test_offline_ci.py > $out/run$i.log 2>&1; rc=$?
  e39=$(grep -c 'Errno 39' $out/run$i.log)
  echo "run$i rc=$rc errno39=$e39 $(grep -E '^(OK|FAILED)' $out/run$i.log)" >> $out/summary.txt
done
echo "leftover_tmp_entries=$(ls -A $out/tmp | wc -l)" >> $out/summary.txt
